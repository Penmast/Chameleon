try:
    import speedtest
except:
    pass


def returnSpeedTestResult():
    try:
        servers = []
        # If you want to test against a specific server
        # servers = [1234]

        s = speedtest.Speedtest() # Speedtest object

        s.get_servers(servers) # Retrieve all the servers

        s.get_best_server() # Gets the closest server

        s.download() # Test the download and gives the result in bits/second

        s.upload() # Test the upload and gives the result in bits/second

        s.results.share() # Create a png file placed of the speedtest.net server

        results_dict = s.results.dict() # Puts the result into a dictionary

        return results_dict
    except:
        return None
