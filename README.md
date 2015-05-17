# pYNAB

A minimalistic library designed to provide native access to YNAB data from Python.

# Install

The simplest way is to install the latest version from PyPI index:

```sh
> pip install -U pynab
```

or install from the latest source:

```sh
git clone https://github.com/aldanor/pynab.git
cd pynab
python setup.py install
```

# Examples

Load the shared YNAB budget:

```python
>>> from ynab import YNAB
>>> ynab = YNAB('~/Dropbox/YNAB', 'MyBudget')
```

Get the list of accounts:

```python
>>> ynab.accounts
[<Account: Cash>, <Account: Checking>]
```

Query the balance, the cleared balance and the reconciled balance for cash account:

```python
>>> cash = ynab.accounts['Cash']
>>> cash.balance, cash.cleared_balance, cash.reconciled_balance
(15.38, 24.38, 41.88)
```

Find the total of all reconciled cash transactions starting 2 weeks ago:

```python
>>> cash = ynab.accounts['Cash']
>>> sum(cash.transactions.since('2 weeks ago').filter('reconciled').amount)
-22.0
```

Find the average amount of all Starbucks purchases in 2015:

```python
>>> starbucks = ynab.payees['Starbucks']
>>> starbucks.transactions.between('2015-01-01', '2015-12-31').amount.mean()
-27.31176470588235
```
