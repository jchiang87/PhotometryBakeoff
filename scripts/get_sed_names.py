def get_sed_names(sed_list):
    """
    Read the sed names from a file with the list of sed filenames
    configured for PhotoZDC1.
    Inputs:
    sed_list = path to file with list of SEDs.
    """
    # Read the names from the sed_list file (which have '.ang'
    # appended for the PhotoZDC1 code).
    sed_names = sorted([x[:-len('.ang\n')] for x in open(sed_list)])
    return sed_names
