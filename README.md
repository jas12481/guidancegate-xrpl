# Trustline-Gated Financial Guidance Agent

A financial guidance AI agent for vulnerable users (special-needs individuals and caregivers) that uses XRPL trustlines as explicit on-chain opt-in / consent gating to create a transparent, portable safety boundary.

## Overview

This agent only surfaces financial resources from verified issuers that users have explicitly opted into via XRPL trustlines. Users create trustlines (explicit on-chain opt-in) to verified issuers, creating permissioned access flows. The agent only shows resources from issuers the user has opted into, ensuring safe, transparent, on-chain permission management.

## Core Architecture

### Required On-Chain Action
- **Guidance issuer trustline**: Required explicit opt-in to access financial guidance resources
- This is the only trustline that gates access

### Payment Mechanism
- **XRP Payments**: Users pay for products/services directly in XRP
- Payments are sent from user wallet to issuer address via XRPL Payment transactions
- All transactions are recorded on-chain and verifiable

## How It Works

### 1. Explicit Opt-In via Trustlines
Users create XRPL trustlines to verified issuers through blockchain transactions. This is not just an app setting—it's an on-chain action that:
- Creates a permanent, auditable consent record
- Can be verified by anyone
- Works across any XRPL-compatible service

### 2. Trustline-Gated Resources
The agent only surfaces financial resources from issuers the user has trustlined. This creates a hard boundary: no trustline = no access.

### 3. XRP Payment Integration
- Users purchase products/services using XRP payments
- Payments are processed directly on the XRPL ledger
- Transaction memos track which product was purchased

## Technical Implementation

### Technology Stack
- **Language**: Python
- **XRPL Library**: `xrpl-py`
- **Network**: XRPL Testnet (for demo)
- **Agent Platform**: Dify (integration ready)

### XRPL Features Used

This project leverages multiple core XRPL features:

1. **Trustlines (TrustSet Transactions)**
   - Primary mechanism for explicit on-chain opt-in/consent
   - Users create trustlines to verified guidance issuers
   - Creates permanent, auditable consent records on the ledger

2. **AccountLines Queries**
   - Queries user's existing trustlines to verify opt-in status
   - Enables real-time access control based on on-chain state
   - Used by API endpoints to check user permissions

3. **Payment Transactions**
   - XRPL native Payment transactions for product purchases
   - Users pay issuers directly in XRP (e.g., 6 XRP for a product)
   - Transaction memos include product identifiers for tracking
   - Direct on-chain payments from user wallet to issuer address

4. **Crossmark Wallet Integration**
   - Browser extension wallet for user-friendly XRPL interactions
   - Handles trustline creation and payment signing
   - Provides seamless UX similar to MetaMask for Ethereum
   - Enables one-click opt-in and purchase flows

5. **JSON-RPC Client**
   - Direct connection to XRPL Testnet/Mainnet
   - Real-time ledger queries and transaction submission
   - Serverless API endpoints for trustline verification

### Issuer Registry
For MVP we demonstrate with demo guidance issuers; in production these would be verified organisations or registry-backed issuers.

**Verified Guidance Issuers:**
- Community Aid Financial Services (GID) - Foundational financial literacy
- InclusiveCare Finance Network (ICN) - Supported decision-making for disabilities
- CalmBridge Financial Wellbeing (CBW) - Low-pressure financial guidance

## Setup

### Prerequisites
- Python 3.8+
- XRPL testnet account (or use faucet)
- Node.js (for Vercel CLI, optional)

### Installation

```bash
# Clone repository
git clone <repository-url>
cd guidancegate-xrpl

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
   - Issuer addresses are already configured for testnet
   - All issuers use XRPL Testnet addresses

2. For testnet, use XRPL testnet faucet:
   - https://xrpl.org/xrp-testnet-faucet.html

3. Install Crossmark wallet extension:
   - https://crossmark.io
   - Required for opt-in and payment flows

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
6. Demonstrate product purchase flow

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

**Core Functionality:**
- XRPL trustline query and creation via Crossmark wallet
- Guidance issuer trustline as required opt-in mechanism
- Trustline-gated resource access with real-time verification
- XRP payment integration for product purchases
- Setup flow with status checking
- Access control based on on-chain trustlines

**User Experience:**
- AI-powered financial guidance agent (Dify integration)
- One-click opt-in via Crossmark wallet extension
- Product marketplace with XRPL payment integration
- Multiple verified guidance issuers (Community Aid, InclusiveCare, CalmBridge)
- Seamless flow: Chat → Opt-in → Access Resources → Purchase Products

**Technical Implementation:**
- Serverless API endpoints (Vercel deployment)
- Real-time trustline verification
- Crossmark wallet integration for transactions
- Production-ready deployment with CORS support

### 🚀 Future Enhancements (Roadmap)
- Multi-signature support for caregiver co-approval
- Escrow-based allowance release
- Enhanced caregiver tools
- DID integration
- Additional guidance issuers

## Project Structure

```
guidancegate-xrpl/
├── api/                    # Vercel serverless functions
│   ├── check-trustline.py  # Trustline verification endpoint
│   ├── issuer-info.py     # Issuer information endpoint
│   ├── issuer-products.py # Products listing endpoint
│   └── requirements.txt   # API dependencies
├── config/
│   └── issuers.py         # Issuer registry configuration
├── src/
│   ├── xrpl_client.py     # XRPL connection and operations
│   ├── setup_flow.py      # Setup flow management
│   └── access_control.py  # Resource access control
├── ui/                    # Frontend pages
│   ├── opt-in.html        # Opt-in page with Crossmark
│   ├── products.html      # Product marketplace
│   └── test-crossmark.html # Crossmark testing utility
├── demo/                  # Demo and testing scripts
│   ├── demo.py            # Main demo script
│   ├── generate_issuers.py
│   ├── quick_test.py
│   └── setup_issuers.py
├── vercel.json            # Vercel deployment configuration
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── DEPLOYMENT.md         # Deployment instructions
└── QUICKSTART.md         # Quick start guide
```

## Why This Approach?

### Trustlines as Explicit Opt-In
XRPL trustlines provide a native mechanism for explicit, on-chain consent. Unlike app settings, trustlines are:
- **Transparent**: Visible on the public ledger
- **Auditable**: Anyone can verify what issuers a user has opted into
- **Permanent**: Creates a permanent, auditable consent record on the ledger
- **Portable**: Works across any XRPL-compatible service

### XRP Payments for Products
XRPL Payment transactions enable direct on-chain purchases:
- Users pay issuers directly in XRP
- All transactions are recorded on the public ledger
- Transaction memos provide purchase tracking
- No intermediaries - direct wallet-to-wallet payments

## SDG Alignment (BGA Bounty Track)

This project aligns with multiple UN Sustainable Development Goals:

**SDG 1: No Poverty**
- Financial inclusion for vulnerable and underserved populations
- Access to financial education and resources regardless of income level

**SDG 3: Good Health & Well-being**
- Supports mental health through CalmBridge Financial Wellbeing
- Reduces financial stress and anxiety

**SDG 4: Quality Education**
- Financial literacy education for all
- Accessible learning resources for special needs individuals

**SDG 10: Reduced Inequalities**
- Financial inclusion for individuals with disabilities (InclusiveCare)
- Support for caregivers managing shared finances
- Non-predatory financial guidance for vulnerable users

**SDG 16: Peace, Justice & Strong Institutions**
- Transparent, on-chain consent mechanisms
- Auditable financial guidance relationships
- User control and data sovereignty

## Contributing

This is a hackathon project. For production use, consider:
- Verified issuer registry
- Multi-signature support
- Enhanced security measures
- Production-grade error handling

## License

[Add your license here]

## Complete User Flow

1. **User interacts with Dify AI agent** → Requests financial guidance
2. **Agent checks trustline status** → Calls `/api/check-trustline` endpoint
3. **If no trustline** → Agent provides opt-in link
4. **User clicks opt-in link** → Opens `/ui/opt-in.html?issuer=community_aid`
5. **User connects Crossmark wallet** → Signs TrustSet transaction
6. **Trustline created on XRPL** → Transaction confirmed on ledger
7. **User returns to agent** → Agent verifies trustline, grants access
8. **Agent suggests products** → Provides link to `/ui/products.html?issuer=community_aid`
9. **User browses products** → Connects wallet, views available products
10. **User purchases product** → Signs Payment transaction via Crossmark
11. **Payment confirmed** → User gains access to product resources

## API Endpoints

**Deployed on Vercel:**
- `POST /api/check-trustline` - Verify user's trustline status
- `GET /api/issuer-info?issuer={key}` - Get issuer information
- `GET /api/issuer-products?issuer={key}&wallet_address={address}` - Get products (requires trustline)

**UI Pages:**
- `/ui/opt-in.html?issuer={key}` - Opt-in page with Crossmark integration
- `/ui/products.html?issuer={key}` - Product marketplace with payment integration

## Verified Issuers

1. **Community Aid Financial Services** (GID)
   - Address: `rJcM4kRyvK3wQ8ngYZJ62iZBqbPcVGs8gT`
   - Focus: Foundational financial literacy for vulnerable users

2. **InclusiveCare Finance Network** (ICN)
   - Address: `r9ZZMzNw4Z9bPhkSZ1DhnF13f8jxeE9JCu`
   - Focus: Supported decision-making for individuals with disabilities

3. **CalmBridge Financial Wellbeing** (CBW)
   - Address: `rLZu53zYBYT6fcq38uNcnVYcEeUuBe2Jd4`
   - Focus: Low-pressure financial guidance for anxiety/stress

## Acknowledgments

Built for NUS FinTech Summit 2026 Hackathon (Ripple Challenge & BGA Bounty Track)

