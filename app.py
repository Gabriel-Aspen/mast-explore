import streamlit as st
from astroquery.mast import Observations
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from astropy.visualization import make_lupton_rgb, ZScaleInterval
from astropy.wcs import WCS

st.title("Hubble Data Viewer (MAST on AWS)")

# Sidebar controls
target_name = st.sidebar.text_input("Target Name", value="trappist-1")

# Function to get available instruments and data types for a target
def get_available_options(target):
    """Query MAST to get available instruments and data types for a target"""
    try:
        # Query all HST observations for the target
        obs_table = Observations.query_criteria(
            obs_collection="HST",
            target_name=target
        )
        
        if len(obs_table) == 0:
            return {}, []
        
        # Create a mapping of data product types to instruments
        datatype_to_instruments = {}
        for obs in obs_table:
            datatype = obs['dataproduct_type']
            instrument = obs['instrument_name']
            if datatype not in datatype_to_instruments:
                datatype_to_instruments[datatype] = set()
            datatype_to_instruments[datatype].add(instrument)
        
        # Convert sets to sorted lists
        for datatype in datatype_to_instruments:
            datatype_to_instruments[datatype] = sorted(list(datatype_to_instruments[datatype]))
        
        # Get unique data product types
        available_datatypes = sorted(list(set(obs_table['dataproduct_type'])))
        
        return datatype_to_instruments, available_datatypes
        
    except Exception as e:
        st.error(f"Error querying MAST: {str(e)}")
        return {}, []

# Get available options for the target
datatype_to_instruments, available_datatypes = get_available_options(target_name)

# Show data product type selection first
if available_datatypes:
    st.sidebar.success(f"Found {len(available_datatypes)} data types for {target_name}")
    dataproduct_type = st.sidebar.selectbox(
        "Data Product Type",
        available_datatypes,
        index=0 if available_datatypes else None
    )
else:
    st.sidebar.warning(f"No HST observations found for {target_name}")
    dataproduct_type = st.sidebar.selectbox(
        "Data Product Type",
        ["spectrum", "image", "timeseries"],
        index=0
    )

# Show available instruments for the selected data product type
if dataproduct_type in datatype_to_instruments and datatype_to_instruments[dataproduct_type]:
    available_instruments = datatype_to_instruments[dataproduct_type]
    st.sidebar.success(f"Found {len(available_instruments)} instruments for {dataproduct_type}")
    instrument_name = st.sidebar.selectbox(
        "Instrument",
        available_instruments,
        index=0 if available_instruments else None
    )
else:
    st.sidebar.warning(f"No instruments found for {dataproduct_type} data")
    instrument_name = st.sidebar.selectbox(
        "Instrument",
        ["COS/FUV", "COS/NUV", "STIS/FUV-MAMA", "STIS/NUV-MAMA", "STIS/CCD", "WFC3/UVIS", "WFC3/IR", "ACS/WFC", "ACS/HRC"]
    )

radius = st.sidebar.text_input("Search Radius", value="0.02 deg")

if st.sidebar.button("Fetch Data"):
    with st.spinner("Querying MAST..."):
        # Search for observations
        obs_table = Observations.query_criteria(
            obs_collection="HST",
            instrument_name=instrument_name,
            target_name=target_name,
            dataproduct_type=dataproduct_type
        )

    if len(obs_table) == 0:
        st.error(f"No {dataproduct_type} data found for these parameters.")
    else:
        st.success(f"Found {len(obs_table)} observations.")
        obs_id = obs_table[0]["obsid"]

        # Get products
        products = Observations.get_product_list(obs_id)
        
        if dataproduct_type == "spectrum":
            # Filter for spectrum products
            data_products = Observations.filter_products(
                products, productSubGroupDescription="X1D"
            )
            product_description = "calibrated spectrum (X1D)"
        elif dataproduct_type == "image":
            # Filter for image products (FLC for calibrated images)
            data_products = Observations.filter_products(
                products, productSubGroupDescription="FLC"
            )
            if len(data_products) == 0:
                # Fallback to FLT if FLC not available
                data_products = Observations.filter_products(
                    products, productSubGroupDescription="FLT"
                )
            product_description = "calibrated image (FLC/FLT)"
        else:  # timeseries
            data_products = Observations.filter_products(
                products, productSubGroupDescription="LIGHTCURVE"
            )
            product_description = "lightcurve data"

        if len(data_products) == 0:
            st.error(f"No {product_description} files found for this observation.")
        else:
            with st.spinner(f"Downloading {dataproduct_type} from MAST/AWS..."):
                manifest = Observations.download_products(data_products)
                data_file = manifest["Local Path"][0]

            # Process and display data based on type
            with fits.open(data_file) as hdul:
                if dataproduct_type == "spectrum":
                    # Plot spectrum
                    wavelength = hdul[1].data["WAVELENGTH"][0]
                    flux = hdul[1].data["FLUX"][0]

                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.plot(wavelength, flux, color="black", lw=0.7)
                    ax.set_xlabel("Wavelength (Å)")
                    ax.set_ylabel("Flux (erg/s/cm²/Å)")
                    ax.set_title(f"HST Spectrum: {target_name} ({instrument_name})")
                    st.pyplot(fig)
                    
                elif dataproduct_type == "image":
                    # Display image - find the first extension with data
                    image_data = None
                    for i, hdu in enumerate(hdul):
                        if hdu.data is not None and hasattr(hdu.data, 'shape'):
                            image_data = hdu.data
                            st.info(f"Using data from extension {i} ({hdu.name if hdu.name else 'PRIMARY'})")
                            break
                    
                    if image_data is None:
                        st.error("No image data found in the FITS file.")
                        st.write("Available extensions:", [f"{i}: {hdu.name if hdu.name else 'PRIMARY'} - {type(hdu.data)}" for i, hdu in enumerate(hdul)])
                    else:
                        # Handle different image formats
                        if len(image_data.shape) == 3:
                            # Multi-extension image, use first extension
                            image_data = image_data[0]
                            st.info("Using first slice of 3D data")
                        
                        # Apply scaling for better visualization
                        interval = ZScaleInterval()
                        vmin, vmax = interval.get_limits(image_data)
                        
                        fig, ax = plt.subplots(figsize=(10, 8))
                        im = ax.imshow(image_data, cmap='viridis', vmin=vmin, vmax=vmax, origin='lower')
                        ax.set_title(f"HST Image: {target_name} ({instrument_name})")
                        ax.set_xlabel("X (pixels)")
                        ax.set_ylabel("Y (pixels)")
                        
                        # Add colorbar
                        cbar = plt.colorbar(im, ax=ax)
                        cbar.set_label("Counts")
                        
                        st.pyplot(fig)
                        
                        # Display image statistics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Mean", f"{np.mean(image_data):.2f}")
                        with col2:
                            st.metric("Std Dev", f"{np.std(image_data):.2f}")
                        with col3:
                            st.metric("Max", f"{np.max(image_data):.2f}")
                        
                else:  # timeseries
                    # Handle timeseries data (basic implementation)
                    st.info("Timeseries data visualization not yet implemented.")
                    st.write("Available extensions:", [hdu.name for hdu in hdul])
                    st.write("Data shape:", hdul[0].data.shape if hdul[0].data is not None else "No data")

