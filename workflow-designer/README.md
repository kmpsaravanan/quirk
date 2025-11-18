# JioSign Visual Workflow Designer

A powerful visual workflow designer for the JioSign platform that allows users to create, design, and deploy workflows using a drag-and-drop interface.

## Features

- 🎨 **Visual Workflow Designer**: Drag-and-drop interface for creating workflows
- 📋 **Component Library**: Pre-built components including:
  - Document Upload
  - Digital Signature
  - Email Notification
  - Approval Gates
  - Conditional Branches
  - Archive Document
  - Webhooks
  - Data Transform
  - And more...
- 💾 **Save & Load**: Save workflows and load them later
- 🚀 **Deployment**: Deploy workflows to Business Accounts
- 📊 **Workflow Management**: View, edit, and manage all workflows
- 🏢 **Business Account Integration**: Deploy workflows at account level

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run app.py
```

Or use the run script:
```bash
chmod +x run.sh
./run.sh
```

## Usage

1. **Design Workflow**: 
   - Select components from the palette
   - Click component buttons to add nodes to canvas
   - Connect nodes to create workflow
   - Save your workflow

2. **My Workflows**:
   - View all saved workflows
   - Edit existing workflows
   - Deploy workflows

3. **Deployments**:
   - Select workflow and business account
   - Deploy workflow
   - Manage active deployments

4. **Business Accounts**:
   - View all business accounts
   - See deployed workflows per account

## Workflow Components

- **Triggers**: Start workflow (Document Upload)
- **Actions**: Perform operations (Digital Signature, Email, Archive)
- **Gateways**: Control flow (Approval Gate, Conditional Branch)
- **End**: Terminate workflow

## File Structure

```
workflow-designer/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── run.sh             # Run script
└── workflows/         # Saved workflows directory (auto-created)
```

## Notes

- Workflows are saved as JSON files in the `workflows/` directory
- Each workflow has a unique ID
- Deployments are tracked at the session level
- Business accounts can have multiple deployed workflows

