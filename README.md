# Trustline-Gated Financial Guidance Agent

A financial guidance AI agent for vulnerable users (special-needs individuals and caregivers) that uses XRPL trustlines as explicit on-chain opt-in / consent gating to create a transparent, portable safety boundary.

## Overview

This agent only surfaces financial resources from verified issuers that users have explicitly opted into via XRPL trustlines. Users create trustlines (explicit on-chain opt-in) to verified issuers, creating permissioned access flows. The agent only shows resources from issuers the user has opted into, ensuring safe, transparent, on-chain permission management.

## Core Architecture

### Required On-Chain Action
- **Guidance issuer trustline**: Required explicit opt-in to access financial guidance resources
- This is the only trustline that gates access

### Optional Enhancement
- **RLUSD trustline**: Optional trustline for enhanced features (balance display, payments)
- Does NOT gate access - resources are available regardless of RLUSD trustline

### Always Available
- **RLUSD as unit of account**: All financial examples use RLUSD as stable reference unit
- No trustline required - RLUSD is used for explanations regardless of trustline status

## How It Works

### 1. Explicit Opt-In via Trustlines
Users create XRPL trustlines to verified issuers through blockchain transactions. This is not just an app setting—it's an on-chain action that:
- Creates a permanent, auditable record
- Can be verified by anyone
- Can be reversed by removing the trustline
- Works across any XRPL-compatible service

### 2. Trustline-Gated Resources
The agent only surfaces financial resources from issuers the user has trustlined. This creates a hard boundary: no trustline = no access.

### 3. RLUSD Integration
- RLUSD trustline is optional (enhancement only)
- RLUSD is always used as unit of account in all financial examples
- Budgeting, allowances, and savings goals are expressed in RLUSD

## Technical Implementation

### Technology Stack
- **Language**: Python
- **XRPL Library**: `xrpl-py`
- **Network**: XRPL Testnet (for demo)
- **Agent Platform**: Dify (integration ready)

### XRPL Features Used
- **Trustlines** (TrustSet transactions): Explicit opt-in mechanism
- **AccountLines queries**: Check existing trustlines
- **RLUSD**: Stable reference unit (optional trustline)

### Issuer Registry
For MVP we demonstrate with a demo guidance issuer; in production this would be a verified organisation or a registry-backed issuer.

**Required Issuer:**
- Guidance issuer: Provides financial guidance resources (required trustline)

**Optional Issuer:**
- RLUSD: Stablecoin for reference unit (optional trustline)

## Setup

### Prerequisites
- Python 3.8+
- XRPL testnet account (or use faucet)
- Node.js (for Vercel CLI, optional)

### Installation

```bash
# Clone repository
git clone <repository-url>
cd jas-finchatbot-app

# Install dependencies
pip install -r requirements.txt
```

### Deployment to Vercel

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

**Quick Deploy:**
1. Push code to GitHub
2. Connect to Vercel
3. Deploy automatically

**Your URLs will be:**
- API: `https://your-app.vercel.app/api/check-trustline`
- Opt-in UI: `https://your-app.vercel.app/ui/opt-in.html?issuer=community_aid`

### Configuration

1. Update issuer addresses in `config/issuers.py`:
   - Replace `rYOUR_ISSUER_ADDRESS` with your test issuer address
   - Replace `rRLUSD_ISSUER_ADDRESS` with RLUSD issuer address (if using)

2. For testnet, use XRPL testnet faucet:
   - https://xrpl.org/xrp-testnet-faucet.html

### Running the Demo

```bash
# Run demo script
python demo/demo.py
```

The demo will:
1. Connect to XRPL testnet
2. Create a test wallet
3. Check setup status
4. Create guidance issuer trustline (required)
5. Check access and show permitted resources
6. Display RLUSD examples (no trustline needed)

## Usage

### Basic Flow

```python
from src.xrpl_client import XRPLClient
from src.setup_flow import SetupFlow
from src.access_control import AccessControl

# Initialize
client = XRPLClient(testnet=True)
setup = SetupFlow(client)
access = AccessControl(client)

# Check setup status
status = setup.check_setup_status(user_address)

# Create required trustline
if not status["setup_complete"]:
    result = setup.create_guidance_issuer_trustline(wallet)

# Check access
access_status = access.check_access(user_address)
if access_status["has_access"]:
    resources = access_status["permitted_resources"]
```

## Key Features

### ✅ MVP Features
- XRPL trustline query and creation
- Guidance issuer trustline as required opt-in
- Trustline-gated resource access
- RLUSD as unit of account (always available)
- Setup flow with status checking
- Access control based on trustlines

### 🚀 Future Enhancements (Roadmap)
- Multi-signature support for caregiver co-approval
- Escrow-based allowance release
- Enhanced caregiver tools
- DID integration
- Multiple guidance issuers

## Project Structure

```
jas-finchatbot-app/
├── config/
│   └── issuers.py          # Issuer registry configuration
├── src/
│   ├── xrpl_client.py      # XRPL connection and operations
│   ├── setup_flow.py       # Setup flow management
│   └── access_control.py   # Resource access control
├── demo/
│   └── demo.py             # Demo script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Why This Approach?

### Trustlines as Explicit Opt-In
XRPL trustlines provide a native mechanism for explicit, on-chain consent. Unlike app settings, trustlines are:
- **Transparent**: Visible on the public ledger
- **Auditable**: Anyone can verify what issuers a user has opted into
- **Reversible**: Users can remove trustlines at any time
- **Portable**: Works across any XRPL-compatible service

### RLUSD as Unit of Account
RLUSD provides a stable reference unit for all financial guidance, ensuring:
- Consistent value representation (1 RLUSD = 1 USD)
- Predictable budgeting examples
- Clear savings goals
- No trustline required for using RLUSD as reference

## Contributing

This is a hackathon project. For production use, consider:
- Verified issuer registry
- Multi-signature support
- Enhanced security measures
- Production-grade error handling

## License

[Add your license here]

## Acknowledgments

Built for NUS FinTech Summit 2026 Hackathon (Ripple Challenge)

