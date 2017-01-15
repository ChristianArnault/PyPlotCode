#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

The web site to get images from the public ESO database:
  http://archive.eso.org/dss/dss

'''

import sys
import urllib.request, urllib.error, urllib.parse
import numpy as np
from time import sleep
import astropy.wcs

import lib_read_file

def dms(angle):
    """ Convert a floating point angle into textual representation
        Degree:Minute:Second (-> DEC coordinate) """
    degree = int(angle)
    minute = (angle - degree) * 60.0
    second = (minute - int(minute)) * 60.0
    return '[%d:%d:%f]' % (int(degree), int(minute), second)


def hms(angle):
    """ Convert a floating point angle into textual representation
        Hour:Minute:Second (-> RA coordinate) """
    hour = angle*24.0/360.0
    hour2 = int(hour)
    minute = (hour - hour2) * 60.0
    second = (minute - int(minute)) * 60.0
    return '[%d:%d:%f]' % (int(hour2), int(minute), second)


def radec(coord):
    """ Convert a floating point coordinates into textual representation
        Hour:Minute:Second (-> RA/DEC coordinates) """
    return 'RA=%s DEC=%s' % (hms(coord[0]), dms(coord[1]))


def get_wcs(image):
    """ Parse the WCS keywords from the primary HDU of an FITS image """

    header = lib_read_file.read_header(image)
    wcs_ = astropy.wcs.WCS(header)

    return wcs_

def convert_to_radec(wcs, x, y):
    '''
    :param wcs:
    :param x:
    :param y:
    :return:
    '''
    pixel = np.array([[x, y],], np.float_)
    sky = wcs.wcs_pix2world(pixel, 0)
    ra, dec = sky[0]
    return ra, dec

def convert_to_xy(wcs, ra, dec):
    '''
    :param wcs:
    :param x:
    :param y:
    :return:
    '''
    coord = np.array([[ra, dec],], np.float_)
    result = wcs.wcs_world2pix(coord, 0)
    x, y = result[0]
    return x, y

def get_celestial_objects(ra, dec, radius):
    '''
    :return:
    '''
    def make_req(ra, dec, radius):
        """
        Build a request tu the Simbad server
        :param ra: floating point value of the RA coordinate
        :param dec: floating point value of the DEC coordinate
        :param radius: floting value of the acceptance radius (degrees)
        :return: request text
        """
        def crep(text, char):
            '''
            :param text: string which must be modified
            :param char: character to be replaced
            :return:
            '''
            text = text.replace(char, '%%%02X' % ord(char))
            return text

        host_simbad = 'simbad.u-strasbg.fr'

        # WGET with the "request" string built as below :

        script = ''
        # output format (for what comes from SIMBAD)
        script += 'format object f1 "'
        script += '%COO(A)'            # hour:minute:second
        script += '\t%COO(D)'          # degree:arcmin:arcsec
        script += '\t%OTYPE(S)'
        script += '\t%IDLIST(1)'
        script += '"\n'

        script += 'query coo '
        script += '%f' % ra           # append "a_ra" (decimal degree)
        script += ' '
        script += '%f' % dec          # append "a_dec" (decimal degree)
        script += ' radius='
        script += '%f' % radius       # append "a_radius" (decimal degree)
        script += 'd'                  # d,m,s
        script += ' frame=FK5 epoch=J2000 equinox=2000' # fk5
        script += '\n'

        # "special characters" converted to "%02X" format :
        script = crep(script, '%')
        script = crep(script, '+')
        script = crep(script, '=')
        script = crep(script, ';')
        script = crep(script, '"')
        script = crep(script, ' ')                # same as upper line.

        script = script.replace('\n', '%0D%0A')    # CR+LF
        script = crep(script, '\t')

        request = 'http://' + host_simbad + '/simbad/sim-script?'
        request += 'script=' + script + '&'

        return request

    def wget(req):
        """
        :param req:
        :return:
        """

        def send(url):
            '''
            :param url:
            :return:
            '''
            retry = 0
            while retry < 10:
                # pylint: disable=broad-except
                try:
                    req = urllib.request.urlopen(url)

                    try:
                        text = req.read()
                        text = text.decode("utf-8")
                        lines = text.split('<BR>\n')
                        return lines[0]
                    except Exception:
                        print('cannot read')
                    except:
                        raise

                except urllib.error.HTTPError:

                    retry += 1
                    sleep(0.2)
                except:
                    raise
            print(retry)

        out = send(req)

        return out

    req = make_req(ra, dec, radius)

    out = wget(req)
    if out is None:
        return '', out, req

    out = out.split('\n')

    in_data = False

    objects = dict()

    for line in out:
        line = line.strip()
        if line == '':
            continue
        if not in_data:
            if line == '::data::'+'::'*36:
                in_data = True
            continue

        data = line.split('\t')

        objects[data[3].strip()] = data[2].strip()

    return objects, out, req

def get_celestial_objects_from_pixels(x, y, wcs, angle):
    '''
    :param x:
    :param y:
    :param wcs:
    :param angle:
    :return:
    '''
    pixel = np.array([[x, y],], np.float_)
    sky = wcs.wcs_pix2world(pixel, 0)
    ra, dec = sky[0]
    objs, out, req = get_celestial_objects(ra, dec, angle)

    return objs, out, req


def tests():
    'Unit tests'
    return 0

if __name__ == '__main__':
    sys.exit(tests())
