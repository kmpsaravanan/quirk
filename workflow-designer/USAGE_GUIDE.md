# JioSign Workflow Designer - Step-by-Step Guide

## 🚀 Quick Start

### Step 1: Create a New Workflow
1. Open the app at `http://localhost:8502`
2. In the sidebar, click **"➕ New Workflow"** button
3. Enter a workflow name in the "Workflow Name" field at the top

### Step 2: Add Components to Canvas
1. Look at the **"📋 Component Palette"** section in the sidebar (left side)
2. **Click any component button** to add it to the canvas:
   - 📄 Document Upload
   - ✍️ Digital Signature
   - 📧 Email Notification
   - ✅ Approval Gate
   - 🔀 Conditional Branch
   - 📦 Archive Document
   - 🔗 Webhook
   - ⏱️ Delay
   - 🔄 Data Transform
   - 🏁 End Workflow

3. Each click adds a new node to the canvas
4. Nodes appear automatically on the canvas

### Step 3: Arrange Nodes on Canvas
1. **Click and drag** any node on the canvas to move it
2. Position nodes to create your workflow flow
3. After moving nodes, click **"💾 Sync Positions"** button to save their positions
4. Nodes will stay in their new positions after syncing

### Step 4: Manage Nodes
1. In the **"Node Management"** section:
   - Select a node from the dropdown
   - Click **"🗑️ Delete Node"** to remove it
   - Click **"🔗 Connect to Next"** to create a connection

### Step 5: Save Your Workflow
1. Click **"💾 Save Workflow"** button (top right)
2. Your workflow is saved with all nodes and positions
3. You can load it later from the sidebar

### Step 6: Deploy Workflow
1. Go to **"My Workflows"** page
2. Find your saved workflow
3. Click **"🚀 Deploy"** button
4. Select a Business Account
5. Click **"🚀 Deploy to Account"**

## 📋 Detailed Instructions

### Adding Components
- **Method 1**: Click component buttons in the sidebar palette
- **Method 2**: Components are added automatically when you click them
- Each component appears as a colored box on the canvas

### Moving Nodes
- **Click** on any node to select it
- **Drag** the node to move it around the canvas
- **Release** to drop it in the new position
- **Click "Sync Positions"** to save the new location

### Creating Workflow Flow
1. Add your first component (usually "Document Upload")
2. Add subsequent components in order
3. Arrange them visually on the canvas
4. Connect nodes using "Connect to Next" button
5. End with "End Workflow" component

### Saving Workflows
- Workflows are saved as JSON files in the `workflows/` folder
- Each workflow has a unique ID
- You can load saved workflows from the sidebar

### Deploying Workflows
- Deploy workflows to Business Accounts
- Each account can have multiple deployed workflows
- Track deployment status in the "Deployments" page

## 🎯 Example Workflow

**Simple Document Signing Workflow:**
1. Add "📄 Document Upload"
2. Add "✍️ Digital Signature"
3. Add "📧 Email Notification"
4. Add "🏁 End Workflow"
5. Arrange them in a line
6. Connect them sequentially
7. Save the workflow
8. Deploy to a Business Account

## 💡 Tips

- **Start Simple**: Begin with 2-3 components
- **Arrange Visually**: Position nodes to show workflow flow
- **Save Often**: Click "Save Workflow" regularly
- **Sync Positions**: Always sync positions after moving nodes
- **Test First**: Use "▶️ Test Workflow" before deploying

## ❓ Troubleshooting

**Nodes not appearing?**
- Make sure you clicked a component button
- Check if "New Workflow" was clicked first
- Refresh the page

**Can't drag nodes?**
- Make sure nodes are rendered on canvas
- Check browser console for errors (F12)
- Try clicking "Sync Positions" first

**Positions not saving?**
- Click "💾 Sync Positions" after moving nodes
- Then click "💾 Save Workflow"
- Check if workflow name is entered

**Can't deploy?**
- Make sure workflow is saved first
- Go to "My Workflows" page
- Select a Business Account

## 🎨 Canvas Features

- **Drag & Drop**: Click and drag nodes to reposition
- **Visual Feedback**: Nodes become semi-transparent while dragging
- **Auto-positioning**: New nodes appear in a grid pattern
- **Color Coding**: Each component type has a unique color
- **Responsive**: Canvas adapts to your screen size

