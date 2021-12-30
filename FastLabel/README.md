# FastTradingLabel

Fast trading label is a tool to quickly label cryptocurrency data, choose the exchange and click on the chart to the rightthe market entry and exit points you consider appropriate

An example is shown below.

![image](https://drive.google.com/uc?export=view&id=1ZEXA1nNtS-fyxa4-tBF1R8hkyJHgU2go)

## Download data

It is very important not to forget to download the data before running the *main.py*, as otherwise we will not be able to choose any exchanges to label.

The data will be downloaded from Binance, to do this we simply need to run the file *data_downloader.py*.
Before running it he needs to insert our *api_key* and *api_secret* by modifying the following dictionary.

for example: 
```python
BINANCE = {
  "key": "5bwyIVmgSoinkU39hx2Mubt8bREkdhdfbdfhdfnfdfn29LNDfw7u57twEUNQLbvQiJBTVu",
  "secret": "AY01aI584hyB77sfXnqx34xDvz9xdhfddfHvZK6evRFze8QWAEdYdhdfdfhDRPsjocUW3Mv"
}
```
