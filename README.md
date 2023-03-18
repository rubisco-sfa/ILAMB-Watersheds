# ILAMB-Watersheds

A collection of ILAMB configure files, code, and data for confronting watershed models with reference data. This work currently requires you to install the `nocollier/watersheds` branch of the [ILAMB](https://github.com/rubisco-sfa/ILAMB) repository. You will also need to install a few additional packages.

```bash
conda install ILAMB
git clone git@github.com:rubisco-sfa/ILAMB.git
cd ILAMB
git checkout nocollier/watersheds
pip install ./
conda install yaml
conda install dataretrieval
```

Feel free to raise [issues](https://github.com/rubisco-sfa/ILAMB-Watersheds/issues) with suggestions for metrics or datasets.
