# 📋 Step-by-Step Guide: Creating a Workflow in JioSign Workflow Designer

## 🎯 Complete Workflow Creation Process

### **STEP 1: Start a New Workflow**

1. **Open the application**
   - Go to: `http://localhost:8502`
   - You'll see the Workflow Designer interface

2. **Create a new workflow**
   - Look at the **left sidebar**
   - Click the **"➕ New Workflow"** button
   - A new workflow ID will be created

3. **Name your workflow**
   - At the top of the main area, you'll see "Workflow Name" field
   - Enter a name like: "Document Signing Workflow"
   - This name will be saved with your workflow

---

### **STEP 2: Add Components to Canvas**

**Method: Click Component Buttons in Sidebar**

1. **Look at the left sidebar** - You'll see "📋 Component Palette"
2. **Click any component button** to add it to the canvas:
   
   Available Components:
   - 📄 **Document Upload** - Start your workflow
   - ✍️ **Digital Signature** - Sign documents
   - 📧 **Email Notification** - Send emails
   - ✅ **Approval Gate** - Require approval
   - 🔀 **Conditional Branch** - Add conditions
   - 📦 **Archive Document** - Archive files
   - 🔗 **Webhook** - Trigger external APIs
   - ⏱️ **Delay** - Add time delays
   - 🔄 **Data Transform** - Transform data
   - 🏁 **End Workflow** - End your workflow

3. **Each click adds a node** to the canvas automatically
4. **Nodes appear** as colored boxes on the canvas

**Example:**
- Click "📄 Document Upload" → Node appears on canvas
- Click "✍️ Digital Signature" → Another node appears
- Click "📧 Email Notification" → Third node appears
- Click "🏁 End Workflow" → Final node appears

---

### **STEP 3: Arrange Nodes on Canvas**

1. **See your nodes** - They appear as colored boxes on the canvas
2. **Click and drag** any node to move it
   - Click on a node
   - Hold mouse button down
   - Drag to new position
   - Release mouse button
3. **Visual feedback** - Node becomes semi-transparent while dragging
4. **Position nodes** to create your workflow flow (left to right, top to bottom)

**Important:** After moving nodes, you MUST:
- Click the **"💾 Sync Positions"** button (below the canvas)
- This saves the new positions
- Without syncing, positions will reset on page refresh

---

### **STEP 4: Connect Nodes (Optional)**

1. **Select a node** from the "Node Management" dropdown
2. **Click "🔗 Connect to Next"** button
3. This creates a connection to the next node in sequence
4. Connections help visualize workflow flow

---

### **STEP 5: Save Your Workflow**

1. **Click "💾 Save Workflow"** button (top right, next to workflow name)
2. You'll see: "✅ Workflow saved successfully!"
3. Your workflow is now saved to the `workflows/` folder
4. You can load it later from the sidebar

---

### **STEP 6: Test Your Workflow**

1. **Click "▶️ Test Workflow"** button (below canvas)
2. This validates your workflow structure
3. You'll see a success message if everything is correct

---

### **STEP 7: Deploy Workflow (Optional)**

1. **Go to "My Workflows"** page (sidebar navigation)
2. **Find your saved workflow** in the list
3. **Click "🚀 Deploy"** button
4. **Select a Business Account** from dropdown
5. **Click "🚀 Deploy to Account"**
6. Your workflow is now deployed and active!

---

## 🎨 Visual Example Workflow

### Simple Document Signing Workflow:

```
[📄 Document Upload] → [✍️ Digital Signature] → [📧 Email Notification] → [🏁 End]
```

**Steps to create:**
1. Click "📄 Document Upload" → Node 1 appears
2. Click "✍️ Digital Signature" → Node 2 appears  
3. Click "📧 Email Notification" → Node 3 appears
4. Click "🏁 End Workflow" → Node 4 appears
5. Drag nodes to arrange them horizontally
6. Click "💾 Sync Positions"
7. Select Node 1, click "🔗 Connect to Next"
8. Select Node 2, click "🔗 Connect to Next"
9. Select Node 3, click "🔗 Connect to Next"
10. Click "💾 Save Workflow"

---

## 💡 Quick Tips

✅ **DO:**
- Click component buttons to add nodes
- Drag nodes to arrange them
- Always sync positions after moving nodes
- Save workflow frequently
- Start with simple workflows (2-3 nodes)

❌ **DON'T:**
- Don't forget to sync positions after dragging
- Don't skip saving your workflow
- Don't create too many nodes at once
- Don't try to drag from sidebar (use buttons instead)

---

## 🔧 Troubleshooting

### **Problem: Nodes not appearing**
- ✅ Make sure you clicked a component button
- ✅ Check if "New Workflow" was clicked first
- ✅ Refresh the page

### **Problem: Can't drag nodes**
- ✅ Make sure nodes are visible on canvas
- ✅ Try clicking on the node first, then drag
- ✅ Check browser console (F12) for errors

### **Problem: Positions not saving**
- ✅ Click "💾 Sync Positions" after moving nodes
- ✅ Then click "💾 Save Workflow"
- ✅ Check if workflow name is entered

### **Problem: Can't see component buttons**
- ✅ Scroll down in the sidebar
- ✅ Make sure you're on "Design Workflow" page
- ✅ Check if sidebar is collapsed (expand it)

---

## 📊 Current Status Indicators

- **Empty Canvas**: Shows instructions
- **Nodes on Canvas**: Shows node count
- **After Dragging**: Click "Sync Positions" to save
- **After Saving**: Success message appears

---

## 🎯 Best Practices

1. **Plan First**: Think about your workflow before creating it
2. **Start Simple**: Begin with 2-3 components
3. **Arrange Visually**: Position nodes to show flow direction
4. **Save Often**: Save your workflow regularly
5. **Test Before Deploy**: Use "Test Workflow" before deploying
6. **Name Clearly**: Use descriptive workflow names

---

## 📝 Summary Checklist

- [ ] Clicked "New Workflow"
- [ ] Entered workflow name
- [ ] Added components by clicking buttons
- [ ] Dragged nodes to arrange them
- [ ] Clicked "Sync Positions"
- [ ] Connected nodes (optional)
- [ ] Clicked "Save Workflow"
- [ ] Tested workflow
- [ ] Deployed to account (optional)

---

**Need Help?** Check the `USAGE_GUIDE.md` for more detailed information!

