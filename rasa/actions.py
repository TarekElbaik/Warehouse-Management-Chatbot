from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import csv
import os

ORDERS_FILE = "../data/orders.csv"
INVENTORY_FILE = "../data/inventory.csv"

# --- Orders ---
def read_orders():
    orders = {}
    try:
        with open(ORDERS_FILE, newline="", encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                orders[row["order_id"]] = row
    except FileNotFoundError:
        print(f"Warning: {ORDERS_FILE} not found")
    except Exception as e:
        print(f"Error reading orders: {e}")
    return orders


def write_orders(orders):
    try:
        with open(ORDERS_FILE, "w", newline="", encoding='utf-8') as csvfile:
            fieldnames = ["order_id", "product_name", "delivery_date", "status"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for order in orders.values():
                writer.writerow(order)
    except Exception as e:
        print(f"Error writing orders: {e}")


# --- Inventory ---
def read_inventory():
    inventory = {}
    try:
        with open(INVENTORY_FILE, newline="", encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                inventory[row["item"]] = {
                    "quantity": int(row["quantity"]),
                    "price": float(row["price"]),
                    "display_name": row["display_name"]
                }
    except FileNotFoundError:
        print(f"Warning: {INVENTORY_FILE} not found")
    except Exception as e:
        print(f"Error reading inventory: {e}")
    return inventory


# --- Actions ---
class ActionCheckOrderStatus(Action):
    def name(self) -> Text:
        return "action_check_order_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        order_id = tracker.get_slot("order_id")
        if not order_id:
            dispatcher.utter_message(text="Please provide the order ID.")
            return []

        orders = read_orders()
        order = orders.get(order_id)
        if order:
            dispatcher.utter_message(
                text=f"✅ Order **{order_id}** is currently *{order['status']}*.\n"
                     f"📦 Product: {order['product_name']}\n"
                     f"📅 Expected delivery date: {order['delivery_date']}."
            )
        else:
            dispatcher.utter_message(text=f"❌ Order {order_id} not found.")
        return []


class ActionRescheduleOrder(Action):
    def name(self) -> Text:
        return "action_reschedule_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        order_id = tracker.get_slot("order_id")
        new_date = tracker.get_slot("date")

        if not order_id or not new_date:
            dispatcher.utter_message(text="Please provide both order ID and new delivery date.")
            return []

        orders = read_orders()
        order = orders.get(order_id)
        if order:
            order["delivery_date"] = new_date
            write_orders(orders)
            dispatcher.utter_message(
                text=f"✅ Order {order_id} delivery date has been successfully updated to {new_date}."
            )
        else:
            dispatcher.utter_message(text=f"❌ Order {order_id} not found.")
        return []


class ActionCheckInventory(Action):
    def name(self) -> Text:
        return "action_check_inventory"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        inventory = read_inventory()

        # Get the item from slot or extract from user message
        item_requested = tracker.get_slot("item_code") or tracker.get_slot("item")
        user_msg = tracker.latest_message.get("text", "").lower().strip()

        # General request keywords
        general_requests = [
            "check stock", "stock", "inventory", "check inventory",
            "show me the inventory", "what items are available",
            "is there any stock left", "cheeck stock"  # typo handling
        ]

        # Normalize item names
        item_names = ["mobile", "laptop", "watch", "charger", "ear-phone", "earphone", "phone"]
        item_codes = ["item1", "item2", "item3", "item4", "item5"]

        has_item_mention = any(item in user_msg for item in item_names + item_codes)

        is_general_request = (
            not item_requested and
            not has_item_mention and
            (user_msg in general_requests or
             any(phrase in user_msg for phrase in general_requests))
        )

        # 1️⃣ List all items if general inventory request
        if is_general_request:
            if not inventory:
                dispatcher.utter_message(text="❌ No inventory data available.")
                return []

            message = "📋 **Available Items:**\n\n"
            for item_id, details in inventory.items():
                qty_status = f"{details['quantity']} in stock" if details['quantity'] > 0 else "Out of stock"
                message += f"• {details['display_name']} — ${details['price']} \n"

            dispatcher.utter_message(text=message.strip())
            dispatcher.utter_message(text="Which specific item would you like to check?")
            return []

        # 2️⃣ Search for specific item
        search_term = None
        if item_requested:
            search_term = item_requested.lower()
        elif has_item_mention:
            for item in item_names + item_codes:
                if item in user_msg:
                    search_term = item
                    break

        if not search_term:
            dispatcher.utter_message(
                text="❌ I couldn't understand which item you're looking for. "
                     "Please try 'check stock' to see all items."
            )
            return []

        matched_item = None

        # Search logic
        for item_id, details in inventory.items():
            display_name_lower = details['display_name'].lower()
            item_id_lower = item_id.lower()

            if (search_term == item_id_lower or
                search_term == display_name_lower or
                (search_term == "phone" and display_name_lower == "mobile")):  # phone → mobile
                matched_item = (item_id, details)
                break

            if search_term in display_name_lower or search_term in item_id_lower:
                matched_item = (item_id, details)
                break

        if matched_item:
            item_id, details = matched_item
            qty = details["quantity"]
            if qty > 0:
                dispatcher.utter_message(
                    text=f"✅ {details['display_name']} is in stock!\n"
                         f"📦 Quantity available: {qty} units\n"
                         f"💲 Price: ${details['price']} each"
                )
            else:
                dispatcher.utter_message(
                    text=f"⚠️ Sorry, {details['display_name']} is currently out of stock."
                )
        else:
            dispatcher.utter_message(
                text=f"❌ Sorry, I couldn't find an item matching '{search_term}'.\n\n"
                     "Please type 'check inventory' to see all available items, or try searching by name."
            )

        return []

