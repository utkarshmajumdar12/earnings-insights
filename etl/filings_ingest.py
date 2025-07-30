import glob
import os

def get_latest_xbrl_files(download_root, cik=None, filing_type="10-Q"):
    """
    Returns list of paths to XBRL (.xml) files just downloaded.
    """
    base_dir = os.path.join(download_root, cik or "", filing_type)
    # get all .xml files in all subdirectories
    xbrl_files = glob.glob(os.path.join(base_dir, '**', '*.xml'), recursive=True)
    return xbrl_files

def ingest():
    for ticker, cik in latest_cik_list().items():
        dl.get("10-Q", ticker, limit=1)
        # find XBRL file(s) in the download directory
        xbrl_files = get_latest_xbrl_files(dl.destination_directory, cik, "10-Q")
        for p in xbrl_files:
            row = parse_xbrl(p)
            row.update({"ticker": ticker, "cik": cik})
            load_star(row)
