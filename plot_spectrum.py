from astroquery.mast import Observations
from astropy.io import fits
import matplotlib.pyplot as plt

# Search for Hubble COS/FUV spectra of quasar 3C273
obs_table = Observations.query_criteria(
    obs_collection="HST",
    instrument_name="COS/FUV",
    target_name="3C273",
    dataproduct_type="spectrum"
)

# Pick first observation
obs_id = obs_table[0]["obsid"]
products = Observations.get_product_list(obs_id)

# Filter for calibrated spectrum (X1D products)
spec_products = Observations.filter_products(
    products, productSubGroupDescription="X1D"
)

# Download
manifest = Observations.download_products(spec_products)
spec_file = manifest["Local Path"][0]

# Open FITS and plot
with fits.open(spec_file) as hdul:
    wavelength = hdul[1].data["WAVELENGTH"][0]
    flux = hdul[1].data["FLUX"][0]

plt.figure(figsize=(10,5))
plt.plot(wavelength, flux, color="black", lw=0.7)
plt.xlabel("Wavelength (Å)")
plt.ylabel("Flux (erg/s/cm²/Å)")
plt.title("Hubble COS Spectrum: 3C273")
plt.show()

