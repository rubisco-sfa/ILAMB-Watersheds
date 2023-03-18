"""The raw MODIS data can be obtained via a submission here:

https://appeears.earthdatacloud.nasa.gov/

However, these files require some processing to be used in ILAMB. I am assuming
that the given data units of 'kg_C_/m^2' mean that they are reporting total gpp
for the 8 day period.
"""
import cftime
import numpy as np
import xarray as xr

ds = xr.open_dataset("MOD17A2HGF.061_500m_aid0001.nc")
da = ds["Gpp_500m"]

# By inspection, it seems a few cells report values of ~3, which are far above
# the majority of the dataset. So I am manually removing them by setting a hand
# threshold of 0.5.
da = xr.where(da < 0.5, da, np.nan, keep_attrs=True)

# We need to test what this does exactly. Because the samples are every 8-days,
# resampling to monthly is convenient for use in ILAMB, but how are they
# clipping days? Need to verify this.
da = da.resample(time="1M").sum() / 30.0

# If null for all time, then set this to null in our product
da = xr.where(
    ds["Gpp_500m"].isnull().all(dim="time") == False, da, np.nan, keep_attrs=True
)

# Prepare data for ILAMB-ready netCDF file
da.attrs["units"] = "kg m-2 d-1"
da.name = "gpp"
da = da.transpose("time", "lat", "lon")
out = xr.Dataset({"gpp": da})
out["time_bounds"] = xr.DataArray(
    np.asarray(
        [
            [
                cftime.DatetimeJulian(y, m, 1)
                for y, m in zip(out["time.year"], out["time.month"])
            ],
            [
                cftime.DatetimeJulian(
                    y if m < 12 else y + 1, (m + 1) if m < 12 else 1, 1
                )
                for y, m in zip(out["time.year"], out["time.month"])
            ],
        ]
    ).T,
    dims=("time", "nb"),
)
out["time"].attrs["bounds"] = "time_bounds"
out.attrs = ds.attrs
out["time"].encoding["units"] = "days since 1980-1-1"
out["time_bounds"].encoding["units"] = "days since 1980-1-1"
out.to_netcdf("AmericanRiverWashington.nc")
