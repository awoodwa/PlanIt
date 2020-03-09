import os.path


def config_file(apikey):
    """
    Function builds an '.hscfg' file allowing user access to NREL data

    INPUT: api key
    OUTPUT: '.hscfg' file in user's home directory
    """
    save_path = os.path.expanduser(
        "~")  # this should be the users home directory
    path = os.path.join(save_path, ".hscfg")
    fnew = open(path, "w+")
    fnew.write(
        "hs_endpoint = https://developer.nrel.gov/api/hsds \n")
    fnew.write("hs_username = None \n")
    fnew.write("hs_password = Nonev\n")
    fnew.write("hs_api_key = %s \n" % apikey)
    fnew.close()
