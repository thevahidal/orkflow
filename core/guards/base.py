class StateGuard:
    def can_enter(self, instance) -> None:
        """
        Raise ValidationError if entering is forbidden
        """

    def can_exit(self, instance) -> None:
        """
        Raise ValidationError if exiting is forbidden
        """
