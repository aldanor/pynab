# -*- coding: utf-8 -*-

import json
import py.path

from models import Accounts, Payees, MasterCategories, Transactions, Categories


class YNAB(object):
    def __init__(self, data):
        self._accounts = Accounts._from_flat(self, data['accounts'])
        self._payees = Payees._from_flat(self, data['payees'])
        self._master_categories = MasterCategories._from_flat(self, data['masterCategories'])
        self._transactions = Transactions._from_flat(self, data['transactions'])
        self._transactions.sort_by('date')

    @classmethod
    def load(cls, path, budget):
        files = py.path.local(path).visit('{}*.ynab4/data*/*/Budget.yfull'.format(budget))
        data = json.load(max(files, key=lambda f: f.mtime()).open())
        return cls(data)

    @property
    def accounts(self):
        return self._accounts

    @property
    def payees(self):
        return self._payees

    @property
    def master_categories(self):
        return self._master_categories

    @property
    def categories(self):
        return Categories(sc for mc in self.master_categories for sc in mc.categories)

    @property
    def transactions(self):
        return self._transactions
