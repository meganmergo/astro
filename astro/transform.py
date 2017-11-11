"""Coordinate transformations

"""

import numpy as np
from astro import kepler, constants, geodetic
from kinematics import attitude

# TODO: Documentation and unit testing
def dcm_pqw2eci_vector(r, v, mu=constants.earth.mu):
    """Define rotation matrix transforming PQW to ECI given eci vectors

    """
    h_vec, _, ecc_vec = kepler.hne_vec(r, v, mu)
    p_hat = ecc_vec / np.linalg.norm(ecc_vec)
    w_hat = h_vec / np.linalg.norm(h_vec) 
    q_hat = np.cross(w_hat, p_hat)

    dcm = np.stack((p_hat, q_hat, w_hat), axis=1)

    return dcm

#TODO: Documentation and testing
def dcm_pqw2eci_coe(raan, inc, arg_p):
    """Define rotation matrix transforming PQW to ECI given orbital elements

    """
    dcm = attitude.rot3(raan).dot(
            attitude.rot1(inc)).dot(attitude.rot3(arg_p))

    return dcm

#TODO: Documentation and testing
def dcm_sez2ecef(latgd, lon, alt=0):
    dcm = dcm_ecef2sez(latgd, lon)
    return dcm.T

#TODO: Documentation and testing
def dcm_ecef2sez(latgd, lon, alt=0):
    dcm = attitude.rot2(np.pi/2 - latgd, 'r').dot(attitude.rot3(lon, 'r'))
    return dcm

#TODO: Documentation and testing
def dcm_ned2ecef(latgd, lon, alt=0):
    dcm = dcm_ecef2ned(latgd, lon, alt)
    return dcm.T

#TODO: Documentation and testing
def dcm_ecef2ned(latgd, lon, alt=0):
    dcm = np.array([[-np.sin(latgd)*np.cos(lon), -np.sin(lon), -np.cos(latgd)*np.cos(lon)],
                    [-np.sin(latgd)*np.sin(lon), np.cos(lon), -np.cos(latgd)*np.sin(lon)],
                    [np.cos(latgd), 0, -np.sin(latgd)]]).T
    return dcm

#TODO: Documentation and testing
def dcm_ecef2enu(latgd, lon, alt=0):
    dcm = np.array([[-np.sin(lon), np.cos(lon), 0],
                    [-np.sin(latgd)*np.cos(lon), -np.sin(latgd)*np.sin(lon), np.cos(latgd)],
                    [np.cos(latgd)*np.cos(lon), np.cos(latgd)*np.sin(lon), np.sin(latgd)]])

    return dcm

#TODO: Documentation and testing
def dcm_enu2ecef(latgd, lon, alt=0):
    dcm = dcm_ecef2enu(latgd, lon, alt)
    return dcm.T

# TODO: Add documentation and testing
# TODO: Make this vectorized to allow for vector inputs
def enu2ecefv(enu, latgd, lon, alt=0):

    # find rotation matrix for this location enu2ecef
    dcm_enu2ecef = dcm_enu2ecef(latgd, lon)

    # vector to site (latgd, lon)
    site_ecef = geodetic.lla2ecef(lat, lon, alt)

    # transform
    ecef = dcm_ecef2enu.dot(enu) + site_ecef

    return ecef

# TODO: Add documentation and testing
# TODO: Make this vectorized to allow for vector inputs
def ecef2enuv(ecef, latgd, lon, alt=0):
    dcm_ecef2enu = dcm_ecef2enu(latgd, lon)

    # site vector
    site_ecef = geodetic.lla2ecef(lat, lon, alt)

    # transform
    enu = dcm_ecef2enu.dot(ecef - site_ecef)
    return enu
