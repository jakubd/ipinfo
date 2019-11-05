import ipinfo.geoipupdater

gipu = ipinfo.geoipupdater.GeoIpUpdater()

print("updating geoip databases to directory: %s" % gipu.cfg.get_geoip_dir())
gipu.force_update()
print("done!")

def stub():
    pass
