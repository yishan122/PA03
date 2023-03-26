import pytest
import os
from datetime import date
from transaction import Transaction

def test_add():
    db = Transaction('test.db')
    db.add({
        'id': 1, 
        'item #': 'Item 1', 
        'amount': 10, 
        'category': 'Food', 
        'date': date.today(), 
        'description': 'Groceries'})
    
    db.add({
        'id': 2, 
        'item #': 'Item 2', 
        'amount': 25, 
        'category': 'Entertainment', 
        'date': date.today(), 
        'description': 'Movie tickets'})
    results = db.select_all()
    print(results)
    assert len(results) == 2
    assert results[0]['item #'] == 'Item 1'
    assert results[1]['category'] == 'Entertainment'
    os.remove('test.db')

def test_select_all():
    db = Transaction('test1.db')
    db.add({
        'id': 1, 
        'item #': 'Item 1', 
        'amount': 10, 
        'category': 'Food', 
        'date': date.today(), 
        'description': 'Groceries'})
    db.add({
        'id': 2, 
        'item #': 'Item 2', 
        'amount': 25, 
        'category': 'Entertainment', 
        'date': date.today(), 
        'description': 'Movie tickets'})
    results = db.select_all()
    assert len(results) == 2
    os.remove('test1.db')

def test_selectWhere():
    db = Transaction('test2.db')
    db.add({
        'id': 1, 
        'item #': 'Item 1', 
        'amount': 10, 
        'category': 'Food', 
        'date': date.today(), 
        'description': 'Groceries'})
    db.add({
        'id': 2, 
        'item #': 'Item 2', 
        'amount': 25, 
        'category': 'Entertainment', 
        'date': date.today(), 
        'description': 'Movie tickets'})
    results = db.select_where("category='Entertainment'")
    assert len(results) == 1
    assert results[0]['item #'] == 'Item 2'
    os.remove('test2.db')

def test_delete():
    db = Transaction('test3.db')
    db.add({
        'id': 1, 
        'item #': 'Item 1', 
        'amount': 10, 
        'category': 'Food', 
        'date': date.today(), 
        'description': 'Groceries'})
    db.add({
        'id': 2, 
        'item #': 'Item 2', 
        'amount': 25, 
        'category': 'Entertainment', 
        'date': date.today(), 
        'description': 'Movie tickets'})
    db.delete(2)
    results = db.select_all()
    assert len(results) == 1
    assert results[0]['item #'] == 'Item 1'
    os.remove('test3.db')

def test_update():
    db = Transaction('test4.db')
    db.add({
        'id': 1, 
        'item #': 'Item 1', 
        'amount': 10, 
        'category': 'Food', 
        'date': date.today(), 
        'description': 'Groceries'})
    
    db.update({
        'id': 1, 
        'item #': 'Item 1', 
        'amount': 15, 
        'category': 'Food', 
        'date': date.today(), 
        'description': 'Groceries and snacks'})
    results = db.select_where("amount=15")
    assert len(results) == 1
    assert results[0]['description'] == 'Groceries and snacks'
    os.remove('test4.db')
  
def test_summarize_by_date():
    db = Transaction('test5.db')

    db.add({
        'id': 1,
        'item #': 'Item 1',
        'amount': 10,
        'category': 'Food',
        'date': date(2023,3,22),
        'description': 'Groceries'})

    db.add({
        'id': 2,
        'item #': 'Item 2',
        'amount': 25,
        'category': 'Entertainment',
        'date': date(2023,3,22),
        'description': 'Movie tickets'})

    db.add({
        'id': 3,
        'item #': 'Item 3',
        'amount': 50,
        'category': 'Entertainment',
        'date': date(2023,3,23),
        'description': 'Restaurants'})

    results = db.summarize('date')
    print(results)
    assert len(results) == 2
    assert results[0]['time'] == '22'
    assert results[0]['total'] == 35
    assert results[1]['time'] == '23'
    assert results[1]['total'] == 50
    os.remove('test5.db')

def test_summarize_by_month():
    db = Transaction('test6.db')
    db.add({
        'id': 1,
        'item #': 'Item 1',
        'amount': 10,
        'category': 'Food',
        'date': date(2023,3,22),
        'description': 'Groceries'})

    db.add({
        'id': 2,
        'item #': 'Item 2',
        'amount': 25,
        'category': 'Entertainment',
        'date': date(2023,3,22),
        'description': 'Movie tickets'})

    db.add({
        'id': 3,
        'item #': 'Item 3',
        'amount': 50,
        'category': 'Entertainment',
        'date': date(2023,3,23),
        'description': 'Restaurants'})
    results = db.summarize('month')
    assert len(results) == 1
    os.remove('test6.db')

def test_summarize_by_year():
    db = Transaction('test7.db')
    db.add({
        'id': 1,
        'item #': 'Item 1',
        'amount': 10,
        'category': 'Food',
        'date': date(2023,3,22),
        'description': 'Groceries'})

    db.add({
        'id': 2,
        'item #': 'Item 2',
        'amount': 25,
        'category': 'Entertainment',
        'date': date(2023,3,22),
        'description': 'Movie tickets'})

    db.add({
        'id': 3,
        'item #': 'Item 3',
        'amount': 50,
        'category': 'Entertainment',
        'date': date(2023,3,23),
        'description': 'Restaurants'})
    results = db.summarize('year')
    assert len(results) == 1
    os.remove('test7.db')

def test_summarize_by_category():
    db = Transaction('test8.db')
    db.add({
        'id': 1,
        'item #': 'Item 1',
        'amount': 10,
        'category': 'Food',
        'date': date(2023,3,22),
        'description': 'Groceries'})

    db.add({
        'id': 2,
        'item #': 'Item 2',
        'amount': 25,
        'category': 'Entertainment',
        'date': date(2023,3,22),
        'description': 'Movie tickets'})

    db.add({
        'id': 3,
        'item #': 'Item 3',
        'amount': 50,
        'category': 'Entertainment',
        'date': date(2023,3,23),
        'description': 'Restaurants'})
    results = db.summarize('category')
    assert len(results) == 2
    os.remove('test8.db')
