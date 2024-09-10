from criptoControl.models import db, Wallet, Cryptocurrency, WalletBalance, Transaction, Price
from criptoControl import app

from flask import Flask, send_file, render_template
import io
import matplotlib.pyplot as plt
from sqlalchemy import func


app = Flask(__name__)

