# Quick Start Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Configure Issuers

Edit `config/issuers.py` and update:
- `rYOUR_ISSUER_ADDRESS` - Your test guidance issuer address
- `rRLUSD_ISSUER_ADDRESS` - RLUSD issuer address (optional)

## Step 3: Get Testnet Wallet

### Option A: Generate New Wallet (Recommended for Demo)
The demo script will automatically generate a wallet from the testnet faucet.

### Option B: Use Existing Wallet
If you have a testnet wallet seed:
```python
from src.xrpl_client import XRPLClient
client = XRPLClient(testnet=True)
wallet = client.import_wallet("sYourSeedHere...")
```

## Step 4: Run Demo

```bash
python demo/demo.py
```

## Step 5: Test the Flow

The demo will:
1. ✅ Connect to XRPL testnet
2. ✅ Create test wallet
3. ✅ Check setup status
4. ✅ Create guidance issuer trustline (required)
5. ✅ Check access and show resources
6. ✅ Display RLUSD examples

## Troubleshooting

### "Cannot connect to XRPL"
- Check internet connection
- Verify testnet URL is accessible
- Try: `https://s.altnet.rippletest.net:51234`

### "Wallet creation failed"
- Testnet faucet may be rate-limited
- Wait a few minutes and try again
- Or use existing testnet wallet seed

### "Trustline creation failed"
- Ensure wallet has sufficient XRP (testnet faucet provides this)
- Check issuer address is correct
- Verify currency code matches issuer

## Next Steps

1. Integrate with Dify agent
2. Add UI for trustline creation
3. Test with multiple issuers
4. Record demo video

