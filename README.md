# Hubble Data Viewer (MAST on AWS)

A Streamlit web application for exploring and visualizing Hubble Space Telescope data from the MAST (Mikulski Archive for Space Telescopes) archive. The app dynamically filters available instruments and data types based on your target, making it easy to discover and visualize HST observations.

## Features

- **Dynamic Filtering**: Automatically shows only instruments and data types available for your target
- **Multi-Data Support**: View spectra, images, and timeseries data
- **Smart Visualization**: 
  - Automatic scaling for optimal image display
  - Professional spectrum plotting
  - Image statistics and analysis
- **User-Friendly Interface**: Clean Streamlit interface with real-time feedback
- **MAST Integration**: Direct access to Hubble data through MAST's AWS infrastructure

## Installation

### Prerequisites

- Python 3.7 or higher
- uv (Python package manager) - [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

### Setup

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd mast
   ```

2. **Install required dependencies**
   ```bash
   uv sync
   ```

   Or install manually:
   ```bash
   uv add streamlit astroquery astropy matplotlib numpy
   ```

## Usage

### Running the App

1. **Start the Streamlit app**:
   ```bash
   uv run streamlit run app.py
   ```

2. **Open your web browser** and navigate to the URL shown in the terminal (typically `http://localhost:8501`)

### How to Use

1. **Enter a Target Name**: 
   - Type the name of an astronomical object (e.g., "trappist-1", "m31", "ngc 1068")
   - The app will automatically query MAST for available observations

2. **Select Data Product Type**:
   - Choose from available data types: spectrum, image, or timeseries
   - Only data types with observations for your target will be shown

3. **Choose an Instrument**:
   - Select from instruments that have the chosen data type for your target
   - The list is dynamically filtered based on your selections

4. **Fetch and View Data**:
   - Click "Fetch Data" to download and visualize the observation
   - For images: View with automatic scaling and statistics
   - For spectra: See wavelength vs. flux plots
   - For timeseries: Basic data information (visualization coming soon)

### Example Targets

Try these popular targets:
- **trappist-1**: Exoplanet system with multiple observations
- **m31**: Andromeda Galaxy (rich in imaging data)
- **ngc 1068**: Active galaxy with spectroscopic data
- **kepler-10**: Exoplanet host star
- **eta carinae**: Evolving star system

## Supported Instruments

The app supports various Hubble instruments including:
- **COS/FUV, COS/NUV**: Cosmic Origins Spectrograph
- **STIS/FUV-MAMA, STIS/NUV-MAMA, STIS/CCD**: Space Telescope Imaging Spectrograph
- **WFC3/UVIS, WFC3/IR**: Wide Field Camera 3
- **ACS/WFC, ACS/HRC**: Advanced Camera for Surveys

## Data Product Types

- **Spectrum**: 1D calibrated spectra (X1D files)
- **Image**: Calibrated images (FLC/FLT files)
- **Timeseries**: Light curve data (basic support)

## Technical Details

- **Backend**: Streamlit web framework
- **Data Source**: MAST (Mikulski Archive for Space Telescopes)
- **Data Format**: FITS files
- **Visualization**: Matplotlib with Astropy integration
- **Scaling**: ZScaleInterval for optimal image display

## Troubleshooting

### Common Issues

1. **No observations found**:
   - Check the target name spelling
   - Try alternative target names (e.g., "m31" vs "andromeda")
   - Some targets may not have HST observations

2. **Installation errors**:
   - Ensure you have Python 3.7+
   - Try updating uv: `uv self update`
   - Install dependencies one by one if needed

3. **Slow loading**:
   - MAST queries can take time for targets with many observations
   - Large image files may take longer to download

### Error Messages

- **"No image data found"**: The FITS file structure may be different than expected
- **"No calibrated spectrum files"**: The observation may not have processed spectrum data
- **"Error querying MAST"**: Check your internet connection and try again

## Contributing

Feel free to contribute improvements:
- Add support for more data product types
- Enhance visualization options
- Improve error handling
- Add new features

## License

This project is open source. Please check individual package licenses for dependencies.

## Acknowledgments

- MAST (Mikulski Archive for Space Telescopes) for providing Hubble data
- Astroquery for MAST API access
- Astropy for astronomical data handling
- Streamlit for the web interface framework
