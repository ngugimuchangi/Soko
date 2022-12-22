#!/usr/bin/python3
""" Console Module """
from cmd import Cmd
from models import storage
from models.cart import Cart
from models.category import Category
from models.chat import Chat
from models.customer import Customer
from models.customer_card import CustomerCard
from models.customer_notification import CustomerNotification
from models.customer import Customer
from models.message import Message
from models.order_detail import OrderDetail
from models.order import Order
from models.product import Product
from models.product_image import ProductImage
from models.review import Review
from models.saved_item import SavedItem
from models.seller_card import SellerCard
from models.seller_notification import SellerNotification
from models.seller import Seller
from models.shipping_address import ShippingAddress
from models.subcategory import Subcategory
from models.transaction import Transaction
from models.transaction_details import TransactionDetail
import re


class SokoConsole(Cmd):
    """ Command line interpreter class
        Private attributes:
            __classes: list of classes
        Public class attributes:
            Cmd.prompt: prompt to display for interactive mode
        Public instance methods:
            Command methods:
                do_create, do_show, do_destroy, do_upate, do_all, do_EOF,
                do_quit
            Help methods:
                help_create, help_show, help_destroy,help_update,
                help_all, help_EOF, help_quit, help_help
            static methods:
    """

    Cmd.prompt = "(soko) "

    classes = {"Customer": Customer, "Cart": Cart,
               "CustomerCard": CustomerCard,
               "CustomerNotification": CustomerNotification,
               "Category": Category, "Chat": Chat, "Order": Order,
               "OrderDetail": OrderDetail, "Message": Message,
               "ProductImage": ProductImage, "Product": Product,
               "Review": Review, "SavedItem": SavedItem,
               "Seller": Seller, "SellerCard": SellerCard,
               "SellerNotification": SellerNotification,
               "ShippingAddress": ShippingAddress,
               "SubCategory": Subcategory, "Transaction": Transaction,
               "TransactionDetail": TransactionDetail
               }

    def do_count(self, line):
        """ Count the number of saved instances
            belonging to a specific class
            Args:
                line (str): class name of objects
                            to count
        """
        if not line:
            print("** class name missing **")
            return

        class_name = line.split()[0]
        if class_name in SokoConsole.classes.keys():
            count = len(storage.search(SokoConsole.classes.get(class_name)))
            print(count)
        else:
            print("** class doesn't exist **")

    def do_create(self, line):
        """ Creates new object instance belonging to
            derived classes of BaseModel
            Args:
                line (str): class name of of object
                            to create
            Return: nothing
        """
        if not line:
            print("** class name missing **")
            return

        class_name = line.split()[0]
        if class_name not in SokoConsole.classes.keys():
            print("** class doesn't exist **")
            return

        args = line.split()[1:]
        if not args:
            print("** missing arguments **")
            return

        kwargs = {}
        for arg in args:
            attr_name = arg.split("=")[0]
            if not hasattr(SokoConsole.classes.get(class_name), attr_name):
                print("** {} {} {} **".format(attr_name,
                      "is not an attribute of", class_name))
                return

            attr_value = arg.split("=")[1:]
            if not attr_value:
                print("** missing attribute value **")
                return

            attr_value = attr_value[0]
            if attr_name in ["quantity", "stock"]:
                attr_value = int(attr_value)
            if attr_name in ["price", "amount", "vat", "shipping_cost",
                             "subtotal"]:
                attr_value = float(attr_value)
            kwargs.update({attr_name: attr_value})

        try:
            new_object = SokoConsole.classes[class_name](**kwargs)
            new_object.save()
        except Exception as error:
            print("** {} **".format(error))
            return
        else:
            print(new_object.id)

    def do_show(self, line):
        """ Display string representation of an instance based
            on the class name and id
            Args:
                line (str): instance"s class name and id
            Return: nothing
        """
        obj = SokoConsole.validate(line)
        if obj:
            print(obj)

    def do_destroy(self, line):
        """ Search and destroy object using its class name and id
            Args:
                line (str): object"s class name and id
            Return: nothing
        """
        obj = SokoConsole.validate(line)
        if obj:
            storage.delete(obj)

    def do_all(self, line):
        """ Display a list of string representations of all objects
            of a specific class or all objects if class is not
            specified
            Args:
                line (str): class name
            Return: nothing
        """
        objects = []
        if not line:
            objects = [str(obj) for obj in storage.search()]
            print(objects)
            return

        class_name = line.split()[0]
        if class_name not in SokoConsole.classes.keys():
            print("** class doesn't exist **")
            return
        objects = [str(obj) for obj in storage.search(SokoConsole.classes.
                   get(class_name))]
        print(objects)

    def do_update(self, line):
        """ Update an object"s existing attribute or add new
            attribute to the object
            Args:
                line (str): class name, object"s id, attribute name,
                            attribute value
            Return: nothing
        """
        obj = SokoConsole.validate(line)
        if not obj:
            return
        update_values = line.split()[2:]
        if not SokoConsole.validate_attr(update_values):
            return
        attr_name, attr_val = update_values[0].split("=")
        if attr_name not in obj.to_dict().keys():
            print("{} {}".format("** Cannot add new attributes.",
                                 "Trying updating existing ones only **"))
            return
        if attr_name in ["created_at", "updated_at"]:
            print("** Cannot update created and updated times manually ")
            return
        if attr_name in ["quantity", "stock"]:
            attr_val = int(attr_val)
        if attr_name in ["price", "amount", "vat",
                         "shipping_cost", "subtotal"]:
            attr_val = float(attr_val)
        setattr(obj, attr_name, attr_val)
        try:
            storage.save()
        except Exception as error:
            print("** {} **".fomart(error))
            return
        print("{} {} {}".format(obj.__class__.__name__,
                                obj.id, "successfully updated"))

    def do_quit(self, line):
        """ Exit program gracefully
            Args: none
            Return: nothing
        """
        storage.close()
        print("{} Goodbye :-)".format(SokoConsole.prompt))
        exit()

    def do_EOF(self, line):
        """ Exit program when receiving terminated signal
            Args: none
            Return: True
        """
        storage.close()
        print("Goodbye :-)")
        return True

    def emptyline(self):
        """ Print new line when user enters no command
            Args: none
            Return: self
        """
        pass

    def help_count(self):
        """ Help function for count command
        """
        print("Usage: <class name>.count().\n" +
              "Count command to count the number of instances",
              "of a specific class\n")

    def help_create(self):
        """ Help function for create command """
        print("Usage: create <class name>",
              "<attr_name>=<attribute_value>\n" +
              "Create command to create new object instance.\n")

    def help_show(self):
        """ Help function for show command """
        print("Usage: show <class name> <id>\n" +
              "Show command to search for object instance by",
              "class and id, and print it.\n")

    def help_destroy(self):
        """ Help function for destroy command """
        print("Usage: destroy <class name > <id>\n" +
              "Destroy command to search for object instance by",
              "class and id, and delete it\n")

    def help_all(self):
        """ Help function for all command """
        print("Usage: all [class name]\n" +
              "Display all objects or all objects of a specific",
              "class\n")

    def help_update(self):
        """ Help function for update command """
        print("Usage: update <class name> <id>=<attribute name>",
              "<attribute value>\n" + "Update command to search for",
              "object by id and update it using passed",
              "attribute name and value\n")

    def help_quit(self):
        """ Help function for quit command """
        print("Quit command to exit the program gracefully\n")

    def help_EOF(self):
        """ Help function for EOF command """
        print("Exit program when Ctrl + D is entered\n")

    def help_help(self):
        """ Help function for help command """
        print("Usage: help [topic/command]\nHelp command to display",
              "information about a commands\n")

    @staticmethod
    def validate(line):
        """ Checks for errors in user input
                1. Class name is specified
                2. Object id is specified
                3. Object with given id is present in storage
            Args:
                line (str): user input
            Return: Object if input passes all validation and
                    object is found
                    None if input fails one of the checks or
                    object is not found
        """
        if not line:
            print("** class name missing **")
            return

        args = line.split()
        class_name = args[0]
        if class_name not in SokoConsole.classes.keys():
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        obj = storage.search(SokoConsole.classes.get(class_name),
                             obj_id)
        if obj:
            return obj
        print("** no instance found **")
        return

    @staticmethod
    def validate_attr(args):
        """ Checks if attribute name and value are passed
            in do_upate method
            Args:
                args: list of arguments
            Return: True if attributes value and names are passed
                    False if either or both are not passed.
        """
        if not args:
            print("** attribute name missing **")
            return False

        args = args[0].split("=")
        if len(args) < 2:
            print("** value missing **")
        elif len(args) > 2:
            print("** too many arguments.",
                  "update one attribute at a time **")
        else:
            return True
        return False


if __name__ == "__main__":
    print("{} Hi! Welcome to Soko CLI".format(SokoConsole.prompt))
    SokoConsole().cmdloop()
