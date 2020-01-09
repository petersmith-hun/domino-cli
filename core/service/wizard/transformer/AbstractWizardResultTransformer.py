from abc import ABCMeta, abstractmethod


class AbstractWizardResultTransformer(object, metaclass=ABCMeta):

    @abstractmethod
    def transform(self, source: dict) -> str:
        pass
