# -*- coding: utf-8 -*-

import re
import os
import json
import string
import warnings

from .models import (Accounts, BudgetMetaData, Categories, FileMetaData,
                     MasterCategories, Payees, Transactions)
from .schema import Device


class YNAB(object):
    def __init__(self, path, budget, device=None):
        """
        Load YNAB budget from the specified path.

        Parameters
        ----------
        path : str
            Path to the budget root, e.g. ~/Documents/YNAB for local budgets or ~/Dropbox/YNAB
            for cloud-synced budgets.
        budget : str
            Budget name.
        device : str (optional)
            Device name -- this corresponds to the .ydevice files in the "devices" folder.
            Can be either A, B, C, ... or a full device name (hostname for desktops). The
            full name can be found in .ydevice files in the "devices" folder. If this
            parameter is not specified, the device with the latest modification time of
            the budget file will be selected.
        """
        root = os.path.abspath(os.path.expanduser(path))
        pattern = re.compile('^' + re.escape(budget) + r'~[A-F0-9]{8}\.ynab4$')
        folders = list(filter(pattern.match, os.listdir(root)))
        if not folders:
            raise RuntimeError('Budget {!r} not found at: {}'.format(budget, path))
        if len(folders) > 1:
            raise RuntimeError('Multiple budgets {!r} found at: {}'.format(budget, path))
        budget_folder = os.path.join(root, folders.pop())
        meta = os.path.join(budget_folder, 'Budget.ymeta')
        with open(meta, 'r') as f:
            data_folder = os.path.join(budget_folder, json.load(f)['relativeDataFolderName'])
        devices_folder = os.path.join(data_folder, 'devices')
        device_files = filter(re.compile(r'^[A-Z]\.ydevice$').match, os.listdir(devices_folder))
        devices = []
        for device_file in device_files:
            with open(os.path.join(devices_folder, device_file), 'r') as f:
                device_data = Device(json.load(f), strict=False)
            guid = device_data.deviceGUID
            budget_file = os.path.join(data_folder, guid, 'Budget.yfull')
            if os.path.isfile(budget_file):
                devices.append({
                    'id': device_data.shortDeviceId,
                    'name': device_data.friendlyName,
                    'file': budget_file,
                    'mtime': os.stat(budget_file).st_mtime,
                    'full': device_data.hasFullKnowledge
                })
        if not devices:
            raise RuntimeError('No valid devices found for {!r} at: {}'.format(budget, path))
        if device is None:
            devices = [d for d in devices if d['full']]
            if not devices:
                raise RuntimeError('No devices with full knowledge found')
            device = max(devices, key=lambda d: d['mtime'])
        else:
            try:
                if device in string.ascii_uppercase:
                    device = [d for d in devices if d['id'] == device].pop()
                else:
                    device = [d for d in devices if d['name'] == device].pop()
                if not device['full']:
                    warnings.warn('Device {!r} does not have full knowledge'.format(d['name']))
            except IndexError:
                raise RuntimeError('No device {!r} for {!r} at: {}'.format(device, budget, path))
        self._path = device['file']
        self._device = device['name']
        with open(self._path, 'r') as f:
            self._init_data(json.load(f))

    @property
    def path(self):
        if not hasattr(self, '_path'):
            return None
        return self._path

    @property
    def device(self):
        if not hasattr(self, '_device'):
            return None
        return self._device

    @classmethod
    def from_json(cls, data):
        """
        Instantiate YNAB object directly from raw JSON data.

        Parameters
        ----------
        data : dict

        Returns
        -------
        ynab : YNAB
        """
        instance = object.__new__(cls)
        instance._init_data(data)
        return instance

    def _init_data(self, data):
        # TODO:
        # - scheduledTransactions
        # - accountMappings
        # - monthlyBudgets
        self._accounts = Accounts._from_flat(self, data['accounts'])
        self._payees = Payees._from_flat(self, data['payees'])
        self._master_categories = MasterCategories._from_flat(self, data['masterCategories'])
        self._transactions = Transactions._from_flat(self, data['transactions'])
        self._transactions.sort_by('date')
        self._meta_data = BudgetMetaData._from_flat(self, data['budgetMetaData'])
        self._file_meta_data = FileMetaData._from_flat(self, data['fileMetaData'])

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

    @property
    def meta_data(self):
        return self._meta_data

    @property
    def precision(self):
        return self._meta_data.precision
