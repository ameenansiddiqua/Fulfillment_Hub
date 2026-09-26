import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="XYZ Fulfillment Hub",
    page_icon="📦",
    layout="wide"
)
st.sidebar.title("📦 Fulfillment Hub")

page = st.sidebar.radio(
    "Navigate to",
    ["Dashboard", "Orders", "Inventory", "Shipments", "Issues"]
)
time_format = st.sidebar.radio(
    "Time Format",
    ["12-hour", "24-hour"]
)
st.title("📦 XYZ Fulfillment Hub")
st.write(
    "A centralized fulfillment dashboard for monitoring orders, "
    "inventory, shipments, priority orders, and operational issues."
)
if time_format == "12-hour":
    current_time = datetime.now().strftime("%d %b %Y, %I:%M %p")
else:
    current_time = datetime.now().strftime("%d %b %Y, %H:%M")

st.caption(f"Last refreshed: {current_time}")

if st.button("🔄 Refresh Dashboard"):
    st.rerun()
orders = pd.read_csv("data/orders.csv")
products = pd.read_csv("data/products.csv")
inventory = pd.read_csv("data/inventory.csv")
shipments = pd.read_csv("data/shipments.csv")
issues = pd.read_csv("data/issues.csv")
if page == "Dashboard":
    total_orders = len(orders)
    priority_orders = len(orders[orders["Priority"] == "Yes"])
    pending_orders = len(orders[orders["Status"] == "Pending"])
    open_issues = len(issues[issues["Status"] == "Open"])

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Orders", total_orders)
    col2.metric("Priority Orders", priority_orders)
    col3.metric("Pending Orders", pending_orders)
    col4.metric("Open Issues", open_issues)

    low_stock_count = len(
        inventory[
            (inventory["Main_Warehouse"] + inventory["Backup_Warehouse"])
            <= inventory["Reorder_Level"]
        ]
    )

    col5.metric("Low Stock", low_stock_count)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Fulfillment Overview")
        status_summary = orders["Status"].value_counts()
        st.bar_chart(status_summary)

    with col2:
        st.subheader("🚚 Shipment Overview")
        shipment_summary = shipments["Shipment_Status"].value_counts()
        st.bar_chart(shipment_summary)


if page == "Orders":
    st.subheader("📋 Orders")
    total_order_count = len(orders)
    pending_order_count = len(
        orders[orders["Status"] == "Pending"]
    )
    priority_order_count = len(
        orders[orders["Priority"] == "Yes"]
    )
    shipped_order_count = len(
        orders[orders["Status"] == "Shipped"]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Orders", total_order_count)
    col2.metric("Pending", pending_order_count)
    col3.metric("Priority", priority_order_count)
    col4.metric("Shipped", shipped_order_count)

    status_filter = st.selectbox(
        "Filter by Order Status",
        ["All"] + sorted(orders["Status"].unique().tolist())
    )

    priority_filter = st.selectbox(
        "Filter by Priority",
        ["All", "Yes", "No"]
    )
    search_order = st.text_input(
        "🔎 Search Order ID, Customer or SKU"
    )

    filtered_orders = orders

    if status_filter != "All":
        filtered_orders = filtered_orders[
            filtered_orders["Status"] == status_filter
        ]

    if priority_filter != "All":
        filtered_orders = filtered_orders[
            filtered_orders["Priority"] == priority_filter
        ]
    if search_order:
        filtered_orders = filtered_orders[
            filtered_orders["Order_ID"].str.contains(
                search_order, case=False, na=False
            )
            |
            filtered_orders["Customer"].str.contains(
                search_order, case=False, na=False
            )
            |
            filtered_orders["SKU"].str.contains(
                search_order, case=False, na=False
            )
        ]
    st.dataframe(
        filtered_orders,
        width="stretch"
    )


if page == "Inventory":
    st.subheader("📦 Inventory")
    total_skus = len(inventory)

    low_stock_items = len(
        inventory[
            (inventory["Main_Warehouse"] + inventory["Backup_Warehouse"])
            <= inventory["Reorder_Level"]
        ]
    )

    available_items = total_skus - low_stock_items

    col1, col2, col3 = st.columns(3)

    col1.metric("Total SKUs", total_skus)
    col2.metric("Low Stock", low_stock_items)
    col3.metric("Available", available_items)

    inventory["Total_Stock"] = (
        inventory["Main_Warehouse"] +
        inventory["Backup_Warehouse"]
    )

    inventory["Stock_Status"] = inventory.apply(
        lambda row: "Low Stock"
        if row["Total_Stock"] <= row["Reorder_Level"]
        else "Available",
        axis=1
    )

    inventory_filter = st.selectbox(
        "Filter by Stock Status",
        ["All", "Low Stock", "Available"]
    )
    search_inventory = st.text_input(
        "🔎 Search Product or SKU"
    )
    if inventory_filter == "All":
        filtered_inventory = inventory
    else:
        filtered_inventory = inventory[
            inventory["Stock_Status"] == inventory_filter
        ]

    if search_inventory:
        filtered_inventory = filtered_inventory[
            filtered_inventory["SKU"].str.contains(
                search_inventory, case=False, na=False
            )
            |
            filtered_inventory["Product_Name"].str.contains(
                search_inventory, case=False, na=False
            )
        ]

    st.dataframe(
        filtered_inventory,
        width="stretch"
    )


if page == "Shipments":
    st.subheader("🚚 Shipments")
    total_shipments = len(shipments)

    picked_up = len(
        shipments[shipments["Pickup_Status"] == "Picked Up"]
    )

    not_shipped = len(
        shipments[shipments["Shipment_Status"] == "Not Shipped"]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Shipments", total_shipments)
    col2.metric("Picked Up", picked_up)
    col3.metric("Not Shipped", not_shipped)

    shipment_filter = st.selectbox(
        "Filter by Shipment Status",
        ["All"] + sorted(shipments["Shipment_Status"].unique().tolist())
    )
    search_shipment = st.text_input(
        "🔎 Search Shipment ID, Order ID or Tracking ID"
    )

    if shipment_filter == "All":
        filtered_shipments = shipments
    else:
        filtered_shipments = shipments[
            shipments["Shipment_Status"] == shipment_filter
        ]
    if search_shipment:
        filtered_shipments = filtered_shipments[
            filtered_shipments["Shipment_ID"].str.contains(
                search_shipment, case=False, na=False
            )
            |
            filtered_shipments["Order_ID"].str.contains(
                search_shipment, case=False, na=False
            )
            |
            filtered_shipments["Tracking_ID"].str.contains(
                search_shipment, case=False, na=False
            )
        ]
    st.dataframe(
        filtered_shipments,
        width="stretch"
    )


if page == "Issues":
    st.subheader("⚠️ Issues")
    total_issues = len(issues)

    open_issue_count = len(
        issues[issues["Status"] == "Open"]
    )

    resolved_issue_count = len(
        issues[issues["Status"] == "Resolved"]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Issues", total_issues)
    col2.metric("Open Issues", open_issue_count)
    col3.metric("Resolved Issues", resolved_issue_count)

    issue_status_filter = st.selectbox(
        "Filter by Issue Status",
        ["All"] + sorted(issues["Status"].unique().tolist())
    )

    if issue_status_filter == "All":
        filtered_issues = issues
    else:
        filtered_issues = issues[
            issues["Status"] == issue_status_filter
        ]

    st.dataframe(
        filtered_issues,
        width="stretch"
    )