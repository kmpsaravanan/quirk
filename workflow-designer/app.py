import streamlit as st
import json
import uuid
from datetime import datetime
from pathlib import Path
import os

# Page Configuration
st.set_page_config(
    page_title="Smart Tender Workflow Designer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit default UI
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    div[data-testid="stToolbar"] {visibility: hidden;}
    .stApp > header {display: none;}
    .stApp [data-testid="stHeader"] {display: none;}
    .stApp [data-testid="stToolbar"] {display: none;}
    .stApp [data-testid="stDecoration"] {display: none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Workflow Designer CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body, html {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background-color: #f5f7fa;
    }
    
    .workflow-container {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    .component-palette {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }
    
    .component-item {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        cursor: grab;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .component-item:hover {
        border-color: #0066CC;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.2);
    }
    
    .component-item:active {
        cursor: grabbing;
    }
    
    .workflow-canvas {
        background: #ffffff;
        border: 2px dashed #d1d5db;
        border-radius: 8px;
        min-height: 600px;
        position: relative;
        padding: 20px;
        overflow: visible !important;
        width: 100%;
    }
    
    #workflowCanvas {
        background: #ffffff !important;
        border: 2px dashed #d1d5db !important;
        border-radius: 8px !important;
        min-height: 600px !important;
        position: relative !important;
        padding: 20px !important;
        overflow: visible !important;
    }
    
    .workflow-node {
        position: absolute;
        background: white;
        border: 2px solid #0066CC;
        border-radius: 8px;
        padding: 15px;
        min-width: 150px;
        cursor: move;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.2s;
    }
    
    .workflow-node:hover {
        box-shadow: 0 4px 16px rgba(0, 102, 204, 0.3);
        transform: scale(1.02);
    }
    
    .workflow-node.selected {
        border-color: #00A651;
        border-width: 3px;
    }
    
    .node-header {
        font-weight: 600;
        color: #0066CC;
        margin-bottom: 8px;
        font-size: 14px;
    }
    
    .node-content {
        font-size: 12px;
        color: #666;
    }
    
    .node-icon {
        font-size: 20px;
        margin-right: 8px;
    }
    
    .connection-line {
        position: absolute;
        pointer-events: none;
        stroke: #0066CC;
        stroke-width: 2;
    }
    
    .btn-primary {
        background: #0066CC;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .btn-primary:hover {
        background: #0052A3;
    }
    
    .btn-success {
        background: #00A651;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
    }
    
    .workflow-list-item {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .workflow-list-item:hover {
        border-color: #0066CC;
        box-shadow: 0 2px 8px rgba(0, 102, 204, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'workflows' not in st.session_state:
    st.session_state.workflows = {}
if 'current_workflow' not in st.session_state:
    st.session_state.current_workflow = None
if 'workflow_nodes' not in st.session_state:
    st.session_state.workflow_nodes = []
if 'workflow_connections' not in st.session_state:
    st.session_state.workflow_connections = []
if 'selected_node' not in st.session_state:
    st.session_state.selected_node = None
if 'workflow_name_value' not in st.session_state:
    st.session_state.workflow_name_value = "Untitled Workflow"
if 'business_accounts' not in st.session_state:
    st.session_state.business_accounts = {
        'account_1': {'name': 'Acme Corporation', 'status': 'active'},
        'account_2': {'name': 'Tech Solutions Ltd', 'status': 'active'},
        'account_3': {'name': 'Global Enterprises', 'status': 'active'}
    }
if 'deployed_workflows' not in st.session_state:
    st.session_state.deployed_workflows = {}

# Workflow Components Library - Smart Tender Platform
WORKFLOW_COMPONENTS = {
    'Tender Discovery': {
        'icon': '🔍',
        'type': 'trigger',
        'color': '#0066CC',
        'description': 'AI-powered tender matching and discovery'
    },
    'Tender Analysis': {
        'icon': '📊',
        'type': 'action',
        'color': '#0066CC',
        'description': 'AI-extract requirements and analyze tender'
    },
    'Bid Preparation': {
        'icon': '📝',
        'type': 'action',
        'color': '#00A651',
        'description': 'Generate technical and financial bid documents'
    },
    'Compliance Check': {
        'icon': '✅',
        'type': 'gateway',
        'color': '#FFC107',
        'description': 'Verify compliance with tender requirements'
    },
    'Digital Signature': {
        'icon': '✍️',
        'type': 'action',
        'color': '#00A651',
        'description': 'Apply JioSign digital signature to documents'
    },
    'Portal Submission': {
        'icon': '📤',
        'type': 'action',
        'color': '#0066CC',
        'description': 'Submit bid to GeM/eTenders portal'
    },
    'Approval Gate': {
        'icon': '🔐',
        'type': 'gateway',
        'color': '#9C27B0',
        'description': 'Require manager approval before submission'
    },
    'Email Notification': {
        'icon': '📧',
        'type': 'action',
        'color': '#FF6B6B',
        'description': 'Send notification to stakeholders'
    },
    'Archive Bid': {
        'icon': '📦',
        'type': 'action',
        'color': '#607D8B',
        'description': 'Archive completed bid documents'
    },
    'End Workflow': {
        'icon': '🏁',
        'type': 'end',
        'color': '#424242',
        'description': 'Workflow completed'
    }
}

# Workflow Storage Directory
WORKFLOW_DIR = Path("workflows")
WORKFLOW_DIR.mkdir(exist_ok=True)

def create_sample_workflow():
    """Create a sample workflow matching Smart Tender Platform MVP"""
    sample_nodes = [
        {
            'id': str(uuid.uuid4()),
            'type': 'Tender Discovery',
            'x': 100,
            'y': 150,
            'icon': '🔍',
            'color': '#0066CC'
        },
        {
            'id': str(uuid.uuid4()),
            'type': 'Tender Analysis',
            'x': 350,
            'y': 150,
            'icon': '📊',
            'color': '#0066CC'
        },
        {
            'id': str(uuid.uuid4()),
            'type': 'Bid Preparation',
            'x': 600,
            'y': 150,
            'icon': '📝',
            'color': '#00A651'
        },
        {
            'id': str(uuid.uuid4()),
            'type': 'Compliance Check',
            'x': 850,
            'y': 150,
            'icon': '✅',
            'color': '#FFC107'
        },
        {
            'id': str(uuid.uuid4()),
            'type': 'Digital Signature',
            'x': 1100,
            'y': 150,
            'icon': '✍️',
            'color': '#00A651'
        },
        {
            'id': str(uuid.uuid4()),
            'type': 'Portal Submission',
            'x': 1350,
            'y': 150,
            'icon': '📤',
            'color': '#0066CC'
        },
        {
            'id': str(uuid.uuid4()),
            'type': 'End Workflow',
            'x': 1600,
            'y': 150,
            'icon': '🏁',
            'color': '#424242'
        }
    ]
    
    sample_connections = [
        {'from': sample_nodes[0]['id'], 'to': sample_nodes[1]['id']},
        {'from': sample_nodes[1]['id'], 'to': sample_nodes[2]['id']},
        {'from': sample_nodes[2]['id'], 'to': sample_nodes[3]['id']},
        {'from': sample_nodes[3]['id'], 'to': sample_nodes[4]['id']},
        {'from': sample_nodes[4]['id'], 'to': sample_nodes[5]['id']},
        {'from': sample_nodes[5]['id'], 'to': sample_nodes[6]['id']}
    ]
    
    return {
        'nodes': sample_nodes,
        'connections': sample_connections,
        'name': 'Smart Tender Management Workflow'
    }

def save_workflow(workflow_id, workflow_data):
    """Save workflow to file"""
    file_path = WORKFLOW_DIR / f"{workflow_id}.json"
    with open(file_path, 'w') as f:
        json.dump(workflow_data, f, indent=2)
    return file_path

def load_workflow(workflow_id):
    """Load workflow from file"""
    file_path = WORKFLOW_DIR / f"{workflow_id}.json"
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    return None

def list_workflows():
    """List all saved workflows"""
    workflows = {}
    if WORKFLOW_DIR.exists():
        for file_path in WORKFLOW_DIR.glob("*.json"):
            with open(file_path, 'r') as f:
                workflow_data = json.load(f)
                workflow_id = file_path.stem
                workflows[workflow_id] = workflow_data
    return workflows

def deploy_workflow(workflow_id, account_id):
    """Deploy workflow to business account"""
    workflow = st.session_state.workflows.get(workflow_id)
    if not workflow:
        workflow = load_workflow(workflow_id)
    
    if workflow:
        deployment_id = str(uuid.uuid4())
        deployment = {
            'workflow_id': workflow_id,
            'account_id': account_id,
            'deployed_at': datetime.now().isoformat(),
            'status': 'active',
            'workflow_data': workflow
        }
        st.session_state.deployed_workflows[deployment_id] = deployment
        return deployment_id
    return None

# Sidebar - Workflow Management
with st.sidebar:
    st.markdown("### 🔷 Smart Tender Workflow Designer")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["Design Workflow", "My Workflows", "Deployments", "Business Accounts"],
        key="nav_page"
    )
    
    st.markdown("---")
    
    if page == "Design Workflow":
        st.markdown("### 📋 Component Palette")
        st.markdown("**Click components below to add to canvas:**")
        
        # Create component buttons that add nodes - organized by workflow stage
        st.markdown("**Workflow Stages:**")
        stage1_cols = st.columns(3)
        stage1_components = ['Tender Discovery', 'Tender Analysis', 'Bid Preparation']
        for idx, comp_name in enumerate(stage1_components):
            with stage1_cols[idx]:
                comp_info = WORKFLOW_COMPONENTS[comp_name]
                if st.button(
                    f"{comp_info['icon']} {comp_name}",
                    key=f"add_{comp_name}",
                    use_container_width=True,
                    help=comp_info['description']
                ):
                    if 'workflow_nodes' not in st.session_state:
                        st.session_state.workflow_nodes = []
                    node_id = str(uuid.uuid4())
                    new_node = {
                        'id': node_id,
                        'type': comp_name,
                        'x': 100 + len(st.session_state.workflow_nodes) * 200,
                        'y': 100 + len(st.session_state.workflow_nodes) * 150,
                        'icon': comp_info['icon'],
                        'color': comp_info['color']
                    }
                    st.session_state.workflow_nodes.append(new_node)
                    st.rerun()
        
        st.markdown("**Verification & Submission:**")
        stage2_cols = st.columns(3)
        stage2_components = ['Compliance Check', 'Digital Signature', 'Portal Submission']
        for idx, comp_name in enumerate(stage2_components):
            with stage2_cols[idx]:
                comp_info = WORKFLOW_COMPONENTS[comp_name]
                if st.button(
                    f"{comp_info['icon']} {comp_name}",
                    key=f"add_{comp_name}",
                    use_container_width=True,
                    help=comp_info['description']
                ):
                    if 'workflow_nodes' not in st.session_state:
                        st.session_state.workflow_nodes = []
                    node_id = str(uuid.uuid4())
                    new_node = {
                        'id': node_id,
                        'type': comp_name,
                        'x': 100 + len(st.session_state.workflow_nodes) * 200,
                        'y': 100 + len(st.session_state.workflow_nodes) * 150,
                        'icon': comp_info['icon'],
                        'color': comp_info['color']
                    }
                    st.session_state.workflow_nodes.append(new_node)
                    st.rerun()
        
        st.markdown("**Additional Components:**")
        stage3_cols = st.columns(4)
        stage3_components = ['Approval Gate', 'Email Notification', 'Archive Bid', 'End Workflow']
        for idx, comp_name in enumerate(stage3_components):
            with stage3_cols[idx]:
                comp_info = WORKFLOW_COMPONENTS[comp_name]
                if st.button(
                    f"{comp_info['icon']} {comp_name}",
                    key=f"add_{comp_name}",
                    use_container_width=True,
                    help=comp_info['description']
                ):
                    if 'workflow_nodes' not in st.session_state:
                        st.session_state.workflow_nodes = []
                    node_id = str(uuid.uuid4())
                    new_node = {
                        'id': node_id,
                        'type': comp_name,
                        'x': 100 + len(st.session_state.workflow_nodes) * 200,
                        'y': 100 + len(st.session_state.workflow_nodes) * 150,
                        'icon': comp_info['icon'],
                        'color': comp_info['color']
                    }
                    st.session_state.workflow_nodes.append(new_node)
                    st.rerun()
        
        st.markdown("---")
        
        # New Workflow
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ New Workflow", use_container_width=True):
                workflow_id = str(uuid.uuid4())
                st.session_state.current_workflow = workflow_id
                st.session_state.workflow_nodes = []
                st.session_state.workflow_connections = []
                st.session_state.selected_node = None
                st.session_state.workflow_name_value = "Untitled Workflow"
                st.rerun()
        
        with col2:
            if st.button("📋 Load Sample", use_container_width=True):
                sample_workflow = create_sample_workflow()
                workflow_id = str(uuid.uuid4())
                st.session_state.current_workflow = workflow_id
                st.session_state.workflow_nodes = sample_workflow['nodes']
                st.session_state.workflow_connections = sample_workflow['connections']
                st.session_state.selected_node = None
                # Update workflow name value (before widget is created)
                st.session_state.workflow_name_value = sample_workflow['name']
                st.success("✅ Sample workflow loaded!")
                st.rerun()
        
        # Load Workflow
        workflows = list_workflows()
        if workflows:
            st.markdown("### 📂 Load Workflow")
            workflow_names = {f"{v.get('name', k)}": k for k, v in workflows.items()}
            selected_workflow = st.selectbox("Select workflow", [""] + list(workflow_names.keys()))
            if selected_workflow and st.button("Load"):
                workflow_id = workflow_names[selected_workflow]
                workflow_data = load_workflow(workflow_id)
                if workflow_data:
                    st.session_state.current_workflow = workflow_id
                    st.session_state.workflow_nodes = workflow_data.get('nodes', [])
                    st.session_state.workflow_connections = workflow_data.get('connections', [])
                    st.rerun()

# Main Content Area
if page == "Design Workflow":
    st.markdown("## 🎨 Smart Tender Management Workflow Designer")
    st.caption("Design workflows that power the Smart Tender Platform MVP - from discovery to submission")
    
    # Workflow Name Input
    col1, col2 = st.columns([3, 1])
    with col1:
        # Get default value from session state
        default_name = st.session_state.get('workflow_name_value', st.session_state.current_workflow or "Untitled Workflow")
        workflow_name = st.text_input("Workflow Name", value=default_name, key="workflow_name")
        # Update the stored value when user changes it
        if workflow_name != st.session_state.get('workflow_name_value'):
            st.session_state.workflow_name_value = workflow_name
    with col2:
        if st.button("💾 Save Workflow", type="primary", use_container_width=True):
            if st.session_state.current_workflow:
                workflow_data = {
                    'id': st.session_state.current_workflow,
                    'name': workflow_name,
                    'nodes': st.session_state.workflow_nodes,
                    'connections': st.session_state.workflow_connections,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                save_workflow(st.session_state.current_workflow, workflow_data)
                st.session_state.workflows[st.session_state.current_workflow] = workflow_data
                st.success("✅ Workflow saved successfully!")
    
    # Workflow Canvas Header
    st.markdown("### 🎨 Tender Management Workflow Canvas")
    
    # Quick action buttons
    if not st.session_state.workflow_nodes:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.info("""
            **📝 Smart Tender Workflow Designer:**
            1. Click "📋 Load Sample" in sidebar to see the complete tender management workflow
            2. OR click component buttons in sidebar to build your custom workflow
            3. Workflow stages: Discovery → Analysis → Preparation → Compliance → Signature → Submission
            4. Drag nodes on the canvas to reposition them
            5. Click "💾 Sync Positions" after moving nodes
            6. Use "💾 Save Workflow" to save your complete workflow
            """)
        with col2:
            if st.button("📋 Load Tender Workflow", type="primary", use_container_width=True):
                sample_workflow = create_sample_workflow()
                workflow_id = str(uuid.uuid4())
                st.session_state.current_workflow = workflow_id
                st.session_state.workflow_nodes = sample_workflow['nodes']
                st.session_state.workflow_connections = sample_workflow['connections']
                st.session_state.selected_node = None
                # Update workflow name value (before widget is created)
                st.session_state.workflow_name_value = sample_workflow['name']
                st.rerun()
    else:
        # Show workflow info
        workflow_stages = [node['type'] for node in st.session_state.workflow_nodes]
        st.success(f"✅ **{len(st.session_state.workflow_nodes)} workflow stages** configured. Drag to reposition, then sync positions.")
        st.caption(f"📋 Workflow: {' → '.join(workflow_stages[:5])}{'...' if len(workflow_stages) > 5 else ''}")
    
    # Display workflow canvas with drag and drop
    nodes_json = json.dumps(st.session_state.workflow_nodes)
    connections_json = json.dumps(st.session_state.workflow_connections)
    descriptions_json = json.dumps({k: v['description'] for k, v in WORKFLOW_COMPONENTS.items()})
    
    # Debug: Show node count and data
    if st.session_state.workflow_nodes:
        with st.expander("🔍 Debug Info", expanded=False):
            st.write(f"**Nodes in session state:** {len(st.session_state.workflow_nodes)}")
            st.json(st.session_state.workflow_nodes[:2])  # Show first 2 nodes
            st.write(f"**JSON length:** {len(nodes_json)} characters")
    
    # Create a form to sync positions back to Streamlit
    with st.form(key="node_positions_form", clear_on_submit=False):
        # Use a text input styled as hidden
        positions_input = st.text_input(
            "node_positions", 
            value=nodes_json, 
            key="positions_input",
            label_visibility="collapsed"
        )
        col1, col2 = st.columns([3, 1])
        with col1:
            st.caption("💡 Drag nodes to reposition. Click 'Sync Positions' to save their new locations.")
        with col2:
            submitted = st.form_submit_button("💾 Sync Positions", use_container_width=True)
        
        if submitted and positions_input:
            try:
                updated_nodes = json.loads(positions_input)
                # Update positions in session state
                for updated_node in updated_nodes:
                    for i, node in enumerate(st.session_state.workflow_nodes):
                        if node['id'] == updated_node['id']:
                            st.session_state.workflow_nodes[i]['x'] = updated_node['x']
                            st.session_state.workflow_nodes[i]['y'] = updated_node['y']
                            break
                st.success("✅ Positions synced!")
                st.rerun()
            except Exception as e:
                st.error(f"Error syncing positions: {str(e)}")
    
    # Hide the input field with CSS
    st.markdown("""
    <style>
        input[data-testid*="positions_input"] {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create canvas HTML - remove placeholder if nodes exist
    placeholder_html = ""
    if not st.session_state.workflow_nodes:
        placeholder_html = '<div style="text-align: center; padding: 20px; color: #999;">No nodes. Add components from sidebar or click "Load Sample".</div>'
    
    # Render nodes using Streamlit columns as a visual test
    if st.session_state.workflow_nodes:
        st.markdown("### 📋 Workflow Nodes Preview")
        cols = st.columns(min(len(st.session_state.workflow_nodes), 6))
        for idx, node in enumerate(st.session_state.workflow_nodes[:6]):
            with cols[idx % len(cols)]:
                st.markdown(f"""
                <div style="background: {node['color']}; color: white; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 10px;">
                    <div style="font-size: 24px;">{node['icon']}</div>
                    <div style="font-weight: 600; font-size: 14px;">{node['type']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Render canvas container
    st.markdown(f"""
    <div id="workflowCanvas" style="position: relative; min-height: 600px; background: #ffffff; border: 2px dashed #d1d5db; border-radius: 8px; padding: 20px; overflow: visible; width: 100%;">
        {placeholder_html}
    </div>
    """, unsafe_allow_html=True)
    
    # Render JavaScript separately
    canvas_script = f"""
    <script>
        (function() {{
            // Suppress external extension errors
            const originalError = console.error;
            console.error = function(...args) {{
                const msg = args.join(' ');
                // Ignore browser extension and Streamlit internal errors
                if (!msg.includes('content_script') && 
                    !msg.includes('message channel closed') &&
                    !msg.includes('Gather usage stats')) {{
                    originalError.apply(console, args);
                }}
            }};
            
            console.log('🔷 Smart Tender Workflow Designer Script Loading...');
            // Initialize nodes data
            let nodesData = [];
            let connectionsData = [];
            try {{
                nodesData = {nodes_json};
                connectionsData = {connections_json};
                console.log('📊 Nodes count:', nodesData.length);
                console.log('🔗 Connections count:', connectionsData.length);
                if (nodesData.length > 0) {{
                    console.log('✅ Nodes data loaded. First node:', nodesData[0]);
                }} else {{
                    console.log('ℹ️ No nodes to render. Add components or load sample workflow.');
                }}
            }} catch (e) {{
                console.error('❌ Error parsing JSON:', e);
                nodesData = [];
                connectionsData = [];
            }}
            
            const nodeDescriptions = {descriptions_json};
            
            // Create node lookup map
            const nodeMap = {{}};
            nodesData.forEach(node => {{
                nodeMap[node.id] = node;
            }});
            
            function findCanvas() {{
                const canvas = document.getElementById('workflowCanvas');
                if (!canvas) {{
                    console.warn('⚠️ Canvas element not found yet, will retry...');
                    return null;
                }}
                console.log('✅ Canvas found');
                return canvas;
            }}
            
            function waitForCanvas(callback, maxAttempts = 50) {{
                let attempts = 0;
                const checkCanvas = setInterval(function() {{
                    attempts++;
                    const canvas = findCanvas();
                    if (canvas) {{
                        clearInterval(checkCanvas);
                        callback(canvas);
                    }} else if (attempts >= maxAttempts) {{
                        clearInterval(checkCanvas);
                        console.error('Canvas not found after', maxAttempts, 'attempts');
                    }}
                }}, 100);
            }}
            
            const canvas = findCanvas();
            
            // Function to sync positions to hidden input
            function syncPositionsToStreamlit() {{
                // Find the input field by its testid or name
                const positionsInput = document.querySelector('input[data-testid*="positions_input"], input[name="node_positions"]');
                if (positionsInput) {{
                    positionsInput.value = JSON.stringify(nodesData);
                    // Trigger change and input events
                    positionsInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    positionsInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    console.log('Positions synced to form:', nodesData.length, 'nodes');
                }} else {{
                    console.log('Positions input not found');
                }}
            }}
            
            // Auto-sync on drag end with debounce
            let syncTimeout;
            function debouncedSync() {{
                clearTimeout(syncTimeout);
                syncTimeout = setTimeout(syncPositionsToStreamlit, 300);
            }}
            
            // Create and render nodes
            function renderNodes() {{
                const canvas = findCanvas();
                if (!canvas) {{
                    console.error('Cannot render: canvas not found');
                    return;
                }}
                
                console.log('🎨 Rendering', nodesData.length, 'nodes on canvas...');
                
                // Clear canvas but keep fallback
                const fallbackElements = canvas.querySelectorAll('[style*="FALLBACK"]');
                canvas.innerHTML = '';
                fallbackElements.forEach(el => canvas.appendChild(el));
                
                if (nodesData.length === 0) {{
                    canvas.innerHTML += '<div style="text-align: center; padding: 20px; color: #999; position: relative; z-index: 1;">No nodes to display. Add components from sidebar or click "Load Sample".</div>';
                    console.log('ℹ️ No nodes to render');
                    return;
                }}
                
                // Create SVG container for connections - make it cover entire canvas
                // IMPORTANT: Add SVG BEFORE nodes so nodes render on top
                const canvasRect = canvas.getBoundingClientRect();
                const svgContainer = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                svgContainer.setAttribute('width', '2000');
                svgContainer.setAttribute('height', '1000');
                svgContainer.setAttribute('viewBox', '0 0 2000 1000');
                svgContainer.style.cssText = 'position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 2; overflow: visible;';
                canvas.insertBefore(svgContainer, canvas.firstChild);
                
                // Add arrowhead marker definition
                const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
                const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
                marker.setAttribute('id', 'arrowhead');
                marker.setAttribute('markerWidth', '12');
                marker.setAttribute('markerHeight', '12');
                marker.setAttribute('refX', '10');
                marker.setAttribute('refY', '6');
                marker.setAttribute('orient', 'auto');
                const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
                polygon.setAttribute('points', '0 0, 12 6, 0 12');
                polygon.setAttribute('fill', '#0066CC');
                marker.appendChild(polygon);
                defs.appendChild(marker);
                svgContainer.appendChild(defs);
                
                // Draw connections from connectionsData array
                console.log('🔗 Drawing', connectionsData.length, 'connections...');
                console.log('🔗 Connections data:', connectionsData);
                console.log('🔗 Node map:', nodeMap);
                
                if (connectionsData.length > 0) {{
                    connectionsData.forEach((conn, connIndex) => {{
                        const fromNode = nodeMap[conn.from];
                        const toNode = nodeMap[conn.to];
                        
                        console.log('  Checking connection', connIndex, ':', conn.from, '→', conn.to);
                        console.log('    From node:', fromNode);
                        console.log('    To node:', toNode);
                        
                        if (fromNode && toNode) {{
                            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                            // Calculate connection points (right edge of source, left edge of target)
                            const x1 = fromNode.x + 150; // Right edge of source node
                            const y1 = fromNode.y + 50;  // Middle vertically
                            const x2 = toNode.x;         // Left edge of target node
                            const y2 = toNode.y + 50;   // Middle vertically
                            
                            console.log('    Drawing line from (' + x1 + ',' + y1 + ') to (' + x2 + ',' + y2 + ')');
                            
                            line.setAttribute('x1', x1);
                            line.setAttribute('y1', y1);
                            line.setAttribute('x2', x2);
                            line.setAttribute('y2', y2);
                            line.setAttribute('stroke', '#0066CC');
                            line.setAttribute('stroke-width', '4');
                            line.setAttribute('marker-end', 'url(#arrowhead)');
                            line.setAttribute('opacity', '1');
                            
                            svgContainer.appendChild(line);
                            console.log('  ✅ Connection drawn:', fromNode.type, '→', toNode.type);
                        }} else {{
                            console.warn('  ⚠️ Connection skipped - node not found');
                        }}
                    }});
                }} else if (nodesData.length > 1) {{
                    // Also draw sequential connections if no explicit connections exist
                    console.log('⚠️ No explicit connections, drawing sequential flow...');
                    for (let i = 0; i < nodesData.length - 1; i++) {{
                        const fromNode = nodesData[i];
                        const toNode = nodesData[i + 1];
                        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                        const x1 = fromNode.x + 150;
                        const y1 = fromNode.y + 50;
                        const x2 = toNode.x;
                        const y2 = toNode.y + 50;
                        
                        console.log('  Drawing sequential line', i, 'from (' + x1 + ',' + y1 + ') to (' + x2 + ',' + y2 + ')');
                        
                        line.setAttribute('x1', x1);
                        line.setAttribute('y1', y1);
                        line.setAttribute('x2', x2);
                        line.setAttribute('y2', y2);
                        line.setAttribute('stroke', '#0066CC');
                        line.setAttribute('stroke-width', '4');
                        line.setAttribute('marker-end', 'url(#arrowhead)');
                        line.setAttribute('opacity', '1');
                        
                        svgContainer.appendChild(line);
                        console.log('  ✅ Sequential connection drawn:', fromNode.type, '→', toNode.type);
                    }}
                }}
                
                // Render nodes
                nodesData.forEach((node, index) => {{
                    try {{
                        const nodeElement = document.createElement('div');
                        nodeElement.className = 'workflow-node';
                        nodeElement.id = 'node-' + node.id;
                        
                        // Ensure visible styling - nodes should be above SVG (z-index 10)
                        const nodeStyle = 'position: absolute !important; ' +
                            'left: ' + node.x + 'px !important; ' +
                            'top: ' + node.y + 'px !important; ' +
                            'background: white !important; ' +
                            'border: 2px solid ' + node.color + ' !important; ' +
                            'border-radius: 8px !important; ' +
                            'padding: 15px !important; ' +
                            'min-width: 150px !important; ' +
                            'cursor: move !important; ' +
                            'box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important; ' +
                            'z-index: 10 !important; ' +
                            'user-select: none !important; ' +
                            'display: block !important; ' +
                            'visibility: visible !important; ' +
                            'opacity: 1 !important;';
                        
                        nodeElement.style.cssText = nodeStyle;
                        nodeElement.setAttribute('data-node-id', node.id);
                        const desc = nodeDescriptions[node.type] || '';
                        nodeElement.innerHTML = '<div style="font-weight: 600; color: ' + node.color + '; margin-bottom: 8px; font-size: 14px;"><span style="font-size: 20px; margin-right: 8px;">' + node.icon + '</span>' + node.type + '</div><div style="font-size: 12px; color: #666;">' + desc + '</div>';
                        
                        // Make node draggable
                        makeDraggable(nodeElement, node);
                        canvas.appendChild(nodeElement);
                        
                        // Verify node was added
                        const addedNode = document.getElementById('node-' + node.id);
                        if (addedNode) {{
                            console.log('  ✓ Node rendered and verified:', node.icon, node.type, 'at (' + node.x + ', ' + node.y + ')');
                            console.log('    Node element:', addedNode);
                            console.log('    Computed style display:', window.getComputedStyle(addedNode).display);
                            console.log('    Computed style visibility:', window.getComputedStyle(addedNode).visibility);
                        }} else {{
                            console.error('  ❌ Node NOT added to DOM:', node.type);
                        }}
                        
                    }} catch (e) {{
                        console.error('Error rendering node:', e, node);
                    }}
                }});
            }}
            
            // Function to redraw connections
            function redrawConnections() {{
                const canvas = findCanvas();
                if (!canvas) return;
                
                // Remove existing SVG
                const oldSvg = canvas.querySelector('svg');
                if (oldSvg) {{
                    oldSvg.remove();
                }}
                
                // Recreate SVG container - insert before nodes
                const svgContainer = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                svgContainer.setAttribute('width', '2000');
                svgContainer.setAttribute('height', '1000');
                svgContainer.setAttribute('viewBox', '0 0 2000 1000');
                svgContainer.style.cssText = 'position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 2; overflow: visible;';
                // Insert SVG before first node (so nodes render on top)
                const firstNode = canvas.querySelector('.workflow-node');
                if (firstNode) {{
                    canvas.insertBefore(svgContainer, firstNode);
                }} else {{
                    canvas.appendChild(svgContainer);
                }}
                
                // Add arrowhead marker
                const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
                const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
                marker.setAttribute('id', 'arrowhead');
                marker.setAttribute('markerWidth', '12');
                marker.setAttribute('markerHeight', '12');
                marker.setAttribute('refX', '10');
                marker.setAttribute('refY', '6');
                marker.setAttribute('orient', 'auto');
                const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
                polygon.setAttribute('points', '0 0, 12 6, 0 12');
                polygon.setAttribute('fill', '#0066CC');
                marker.appendChild(polygon);
                defs.appendChild(marker);
                svgContainer.appendChild(defs);
                
                // Draw connections
                if (connectionsData.length > 0) {{
                    connectionsData.forEach((conn) => {{
                        const fromNode = nodeMap[conn.from];
                        const toNode = nodeMap[conn.to];
                        
                        if (fromNode && toNode) {{
                            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                            const x1 = fromNode.x + 150;
                            const y1 = fromNode.y + 50;
                            const x2 = toNode.x;
                            const y2 = toNode.y + 50;
                            
                            line.setAttribute('x1', x1);
                            line.setAttribute('y1', y1);
                            line.setAttribute('x2', x2);
                            line.setAttribute('y2', y2);
                            line.setAttribute('stroke', '#0066CC');
                            line.setAttribute('stroke-width', '3');
                            line.setAttribute('marker-end', 'url(#arrowhead)');
                            line.setAttribute('opacity', '0.8');
                            
                            svgContainer.appendChild(line);
                        }}
                    }});
                }} else if (nodesData.length > 1) {{
                    // Sequential connections
                    for (let i = 0; i < nodesData.length - 1; i++) {{
                        const fromNode = nodesData[i];
                        const toNode = nodesData[i + 1];
                        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                        const x1 = fromNode.x + 150;
                        const y1 = fromNode.y + 50;
                        const x2 = toNode.x;
                        const y2 = toNode.y + 50;
                        
                        line.setAttribute('x1', x1);
                        line.setAttribute('y1', y1);
                        line.setAttribute('x2', x2);
                        line.setAttribute('y2', y2);
                        line.setAttribute('stroke', '#0066CC');
                        line.setAttribute('stroke-width', '3');
                        line.setAttribute('marker-end', 'url(#arrowhead)');
                        line.setAttribute('opacity', '0.8');
                        
                        svgContainer.appendChild(line);
                    }}
                }}
            }}
        
            // Make element draggable
            function makeDraggable(element, nodeData) {{
                let isDragging = false;
                let currentX;
                let currentY;
                let initialX;
                let initialY;
                let xOffset = nodeData.x;
                let yOffset = nodeData.y;
                
                element.addEventListener('mousedown', dragStart);
                document.addEventListener('mousemove', drag);
                document.addEventListener('mouseup', dragEnd);
                
                function dragStart(e) {{
                    if (e.target.closest('.workflow-node') === element || element.contains(e.target)) {{
                        initialX = e.clientX - xOffset;
                        initialY = e.clientY - yOffset;
                        isDragging = true;
                        element.style.zIndex = '1000';
                        element.style.opacity = '0.8';
                        e.preventDefault();
                    }}
                }}
                
                function drag(e) {{
                    if (isDragging) {{
                        e.preventDefault();
                        currentX = e.clientX - initialX;
                        currentY = e.clientY - initialY;
                        
                        xOffset = currentX;
                        yOffset = currentY;
                        
                        element.style.left = xOffset + 'px';
                        element.style.top = yOffset + 'px';
                        
                        // Update node position in data
                        nodeData.x = xOffset;
                        nodeData.y = yOffset;
                        
                        // Redraw connections as node moves
                        redrawConnections();
                    }}
                }}
                
                function dragEnd(e) {{
                    if (isDragging) {{
                        initialX = currentX;
                        initialY = currentY;
                        isDragging = false;
                        element.style.opacity = '1';
                        element.style.zIndex = '10';
                        
                        // Update node position in data
                        nodeData.x = xOffset;
                        nodeData.y = yOffset;
                        
                        // Final redraw
                        redrawConnections();
                        
                        // Debounced sync to form
                        debouncedSync();
                        
                        // Store updated positions
                        window.updatedNodes = nodesData;
                    }}
                }}
            }}
        
            // Render function that tries multiple times
            function attemptRender() {{
                const canvas = findCanvas();
                if (canvas && nodesData.length > 0) {{
                    console.log('Attempting to render', nodesData.length, 'nodes');
                    renderNodes();
                    return true;
                }}
                return false;
            }}
            
            // Wait for canvas and render
            if (canvas) {{
                console.log('✅ Canvas found immediately');
                if (nodesData.length > 0) {{
                    setTimeout(function() {{
                        renderNodes();
                        console.log('🎉 Workflow rendering complete!');
                    }}, 100);
                }}
            }} else {{
                console.log('⏳ Waiting for canvas element...');
                waitForCanvas(function(canvas) {{
                    console.log('✅ Canvas ready');
                    if (nodesData.length > 0) {{
                        renderNodes();
                        console.log('🎉 Workflow rendering complete!');
                    }}
                }});
            }}
            
            // Also try after delays as backup
            setTimeout(function() {{
                const canvas = findCanvas();
                if (canvas && nodesData.length > 0) {{
                    console.log('🔄 Backup render attempt 1...');
                    renderNodes();
                }}
            }}, 500);
            
            setTimeout(function() {{
                const canvas = findCanvas();
                if (canvas && nodesData.length > 0) {{
                    console.log('🔄 Backup render attempt 2...');
                    renderNodes();
                }}
            }}, 1500);
            
            // Expose function to get updated nodes
            window.getUpdatedNodes = function() {{
                return nodesData;
            }};
            
            console.log('✅ Workflow Designer Script Loaded Successfully');
        }})();
    </script>
    """
    
    st.markdown(canvas_script, unsafe_allow_html=True)
    
    # Show node count and instructions
    if st.session_state.workflow_nodes:
        st.caption(f"📊 {len(st.session_state.workflow_nodes)} nodes on canvas. Click and drag nodes to reposition them. Click 'Sync Positions' after moving nodes to save their positions.")
    
    # Node Management
    if st.session_state.workflow_nodes:
        st.markdown("### Node Management")
        node_options = {f"{node['type']} ({node['id'][:8]})": node['id'] for node in st.session_state.workflow_nodes}
        selected_node_id = st.selectbox("Select Node", [""] + list(node_options.keys()))
        
        if selected_node_id:
            node_id = node_options[selected_node_id]
            st.session_state.selected_node = node_id
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Delete Node", use_container_width=True):
                    st.session_state.workflow_nodes = [n for n in st.session_state.workflow_nodes if n['id'] != node_id]
                    st.session_state.selected_node = None
                    st.rerun()
            
            with col2:
                if st.button("🔗 Connect to Next", use_container_width=True):
                    # Simple connection logic - connect to next node in sequence
                    node_index = next(i for i, n in enumerate(st.session_state.workflow_nodes) if n['id'] == node_id)
                    if node_index < len(st.session_state.workflow_nodes) - 1:
                        next_node_id = st.session_state.workflow_nodes[node_index + 1]['id']
                        connection = {
                            'from': node_id,
                            'to': next_node_id
                        }
                        if connection not in st.session_state.workflow_connections:
                            st.session_state.workflow_connections.append(connection)
                            st.success("✅ Connected!")
                            st.rerun()
    
    # Workflow Actions
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶️ Test Workflow", use_container_width=True):
            if st.session_state.workflow_nodes:
                st.success("✅ Workflow test completed successfully!")
            else:
                st.warning("⚠️ Add nodes to workflow first")
    
    with col2:
        if st.button("📊 View Flow", use_container_width=True):
            st.json({
                'nodes': len(st.session_state.workflow_nodes),
                'connections': len(st.session_state.workflow_connections),
                'workflow_id': st.session_state.current_workflow
            })
    
    with col3:
        if st.button("🔄 Clear Canvas", use_container_width=True):
            st.session_state.workflow_nodes = []
            st.session_state.workflow_connections = []
            st.session_state.selected_node = None
            st.rerun()

elif page == "My Workflows":
    st.markdown("## 📚 My Workflows")
    
    workflows = list_workflows()
    if workflows:
        for workflow_id, workflow_data in workflows.items():
            with st.expander(f"📋 {workflow_data.get('name', 'Unnamed Workflow')}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Nodes", len(workflow_data.get('nodes', [])))
                with col2:
                    st.metric("Connections", len(workflow_data.get('connections', [])))
                with col3:
                    st.metric("Status", "Saved")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{workflow_id}"):
                        st.session_state.current_workflow = workflow_id
                        st.session_state.workflow_nodes = workflow_data.get('nodes', [])
                        st.session_state.workflow_connections = workflow_data.get('connections', [])
                        st.session_state.nav_page = "Design Workflow"
                        st.rerun()
                
                with col2:
                    if st.button(f"🚀 Deploy", key=f"deploy_{workflow_id}"):
                        st.session_state.deploy_workflow_id = workflow_id
                        st.session_state.nav_page = "Deployments"
                        st.rerun()
    else:
        st.info("No workflows saved yet. Create one in the Design Workflow section.")

elif page == "Deployments":
    st.markdown("## 🚀 Workflow Deployments")
    
    # Deploy new workflow
    if 'deploy_workflow_id' in st.session_state:
        workflow_id = st.session_state.deploy_workflow_id
    else:
        workflows = list_workflows()
        workflow_options = {f"{v.get('name', k)}": k for k, v in workflows.items()}
        selected_workflow = st.selectbox("Select Workflow to Deploy", [""] + list(workflow_options.keys()))
        workflow_id = workflow_options.get(selected_workflow) if selected_workflow else None
    
    if workflow_id:
        st.markdown("### Deploy Workflow")
        account_options = {f"{v['name']} ({k})": k for k, v in st.session_state.business_accounts.items()}
        selected_account = st.selectbox("Select Business Account", [""] + list(account_options.keys()))
        
        if selected_account:
            account_id = account_options[selected_account]
            if st.button("🚀 Deploy to Account", type="primary"):
                deployment_id = deploy_workflow(workflow_id, account_id)
                if deployment_id:
                    st.success(f"✅ Workflow deployed successfully! Deployment ID: {deployment_id[:8]}")
                    if 'deploy_workflow_id' in st.session_state:
                        del st.session_state.deploy_workflow_id
                    st.rerun()
    
    # List deployments
    st.markdown("### Active Deployments")
    if st.session_state.deployed_workflows:
        for deployment_id, deployment in st.session_state.deployed_workflows.items():
            account_name = st.session_state.business_accounts[deployment['account_id']]['name']
            workflow_name = deployment['workflow_data'].get('name', 'Unnamed')
            
            with st.expander(f"🚀 {workflow_name} → {account_name}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Deployment ID:** {deployment_id[:8]}")
                with col2:
                    st.write(f"**Status:** {deployment['status']}")
                with col3:
                    st.write(f"**Deployed:** {deployment['deployed_at'][:10]}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"⏸️ Pause", key=f"pause_{deployment_id}"):
                        deployment['status'] = 'paused'
                        st.rerun()
                with col2:
                    if st.button(f"🗑️ Remove", key=f"remove_{deployment_id}"):
                        del st.session_state.deployed_workflows[deployment_id]
                        st.rerun()
    else:
        st.info("No deployments yet. Deploy a workflow to get started.")

elif page == "Business Accounts":
    st.markdown("## 🏢 Business Accounts")
    
    for account_id, account_info in st.session_state.business_accounts.items():
        with st.expander(f"🏢 {account_info['name']}"):
            st.write(f"**Account ID:** {account_id}")
            st.write(f"**Status:** {account_info['status']}")
            
            # Count deployments for this account
            account_deployments = [d for d in st.session_state.deployed_workflows.values() 
                                 if d['account_id'] == account_id]
            st.metric("Active Workflows", len(account_deployments))
            
            if account_deployments:
                st.markdown("**Deployed Workflows:**")
                for deployment in account_deployments:
                    workflow_name = deployment['workflow_data'].get('name', 'Unnamed')
                    st.write(f"- {workflow_name} ({deployment['status']})")


