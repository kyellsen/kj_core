from typing import Type, Dict, Tuple, List, Optional, Union, Any

from kj_logger import get_logger

logger = get_logger(__name__)

from ..utils.base import Base


class CoreBaseClass(Base):
    __abstract__ = True

    def __init__(self):
        super().__init__()
        self._config = None
        self._data_manager = None
        self._database_manager = None
        self._plot_manager = None

    def get_child_attr_name(self) -> Optional[str]:
        """
        Get the attribute name of the children based on the class name.

        Returns
        -------
        str or None
            The attribute name if the class name is found, otherwise None.
        """
        mapping = {
            "Project": "series",
            "Series": "measurement",
            "Measurement": "measurement_version"
        }

        # Store the attribute name corresponding to the class in a variable
        child_attr_name = mapping.get(self.__class__.__name__)

        return child_attr_name

    def get_children_instances(self) -> Optional[List[Any]]:
        """
        Get the child instances of the current class based on the attribute name returned by get_child_attr_name.

        Returns
        -------
        list of any type or None
            A list of child instances if the attribute name is found, otherwise None.
        """
        # Get the attribute name of children using the helper function
        attr_name = self.get_child_attr_name()

        # Retrieve the child instances using the attribute name
        child_instances = getattr(self, attr_name, None) if attr_name else None

        return child_instances

    @staticmethod
    def method_for_all_in_list(instances, method_name, *args: Any, **kwargs: Any) -> List[Any]:
        logger.info(
            f"Applying '{method_name}' to '{len(instances)}' of class '{instances[0].__class__.__name__}'!")
        results: List[Any] = []

        for i in instances:
            method = getattr(i, method_name, None)
            if callable(method):
                try:
                    result = method(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    logger.error(
                        f"Error occurred while executing the method '{method_name}' on '{i}': {e}"
                    )
            else:
                logger.error(f"The method '{method_name}' does not exist in the class '{i.__class__.__name__}'.")
                return []

        return results

    def method_for_all_children(self, method_name, *args: Any, **kwargs: Any) -> List[Any]:
        """
        Call a method on all objects in an attribute list and return the results.

        Args:
            method_name (str): The name of the method to be called.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            List[Any]: A list containing the return values of the method calls.
        """
        children_instances = self.get_children_instances()
        if not children_instances:
            logger.error("No child instances found.")
            return []
        logger.info(
            f"Applying '{method_name}' to '{len(children_instances)}' of class '{children_instances[0].__class__.__name__}'!")
        results: List[Any] = []

        for obj in children_instances:
            method = getattr(obj, method_name, None)
            if callable(method):
                try:
                    result = method(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    logger.error(
                        f"Error occurred while executing the method '{method_name}' on '{obj.__class__.__name__}': {e}"
                    )
            else:
                logger.error(f"The method '{method_name}' does not exist in the class '{obj.__class__.__name__}'.")
                return []

        return results

    def find_all_of_class(self, class_name: str) -> List[Any]:
        """
        Find all instances of a given class within the hierarchy of the current instance.

        Args:
            class_name (str): The name of the class of which instances are to be found.

        Returns:
            List[Any]: A list containing all the found instances of the class.
        """
        if self.__class__.__name__ == class_name:
            return [self]

        found_instances: List[Any] = []
        children_instances = self.get_children_instances()

        if children_instances is not None:
            for child in children_instances:
                try:
                    found_child_instances = child.find_all_of_class(class_name)
                    found_instances.extend(found_child_instances)
                except Exception as e:
                    logger.error(
                        f"Error occurred while executing 'find_all_of_class' on '{child.__class__.__name__}': {e}")

        return found_instances

    def method_for_all_of_class(self, class_name: Optional[str] = None, method_name: Optional[str] = None, *args: Any,
                                **kwargs: Any) -> List[Any]:
        """
        Execute a method on all instances of a specified class and return the results.

        Args:
            class_name (str, optional): The name of the class on which the method should be called. Defaults to the class of self.
            method_name (str, optional): The name of the method to be called. Defaults to '__str__' method of the class.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            List[Any]: A list containing the return values of the method calls.
        """
        class_name = class_name or self.__class__.__name__
        method_name = method_name or '__str__'
        results: List[Any] = []

        instances_of_class = self.find_all_of_class(class_name)
        logger.info(f"Found '{len(instances_of_class)}' instances of class '{class_name}'.")

        for instance in instances_of_class:
            method = getattr(instance, method_name, None)
            if callable(method):
                try:
                    result = method(*args, **kwargs)
                    if isinstance(result, list):
                        results.extend(result)  # Fügen Sie Listen-Elemente hinzu
                    else:
                        results.append(result)  # Fügen Sie einzelne Elemente hinzu
                except Exception as e:
                    logger.error(
                        f"Error occurred while executing the method '{method_name}' on '{instance.__class__.__name__}': {e}"
                    )
            else:
                logger.error(f"The method '{method_name}' does not exist in the class '{instance.__class__.__name__}'.")

        return results
