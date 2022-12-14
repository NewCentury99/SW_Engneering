import tkinter
import tkinter.messagebox

from src.common.ui_util import UIUtil, Position
from src.stock.service.stock_watch_serv import StockWatchServ
from src.stock.ui.stock_detail_ui import StockDetailUI
from src.stock.ui.stock_register_ui import StockRegisterUI


class DashboardUI(tkinter.Tk):
    parent = None
    ui_util = None
    api = None
    stock_watch_serv = None
    task = None

    # UI Fields
    cash_balance_value = None
    today_real_profit_value = None
    watching_list_treeview = None
    stock_balance_treeview = None
    order_logs_treeview = None
    stop_trading_btn = None
    start_trading_btn = None

    def __init__(self, parent_window, api):
        super().__init__()
        self.parent = parent_window
        self.api = api
        self.stock_watch_serv = StockWatchServ(self.api)
        self.setup()

    def setup(self):
        self.title("NewCentury Auto Trader")
        self.ui_util = UIUtil(self, 1615, 850)
        self.geometry(self.ui_util.calc_geometry())
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.launch()
        self.refresh()

    def launch(self):
        title = self.ui_util.make_title("Dashboard")

        cash_balance_label = self.ui_util.make_label(
            "Cash Balance (KRW): ",
            Position(20, 0, 150, 25),
            cst_x=None,
            cst_y=title
        )
        self.cash_balance_value = self.ui_util.make_entry(
            "", Position(5, 0, 150, 25), cash_balance_label, title, True
        )

        today_real_profit_label = self.ui_util.make_label(
            "Today's Realized Profit (KRW): ",
            Position(20, 0, 200, 25),
            cst_x=self.cash_balance_value,
            cst_y=title
        )
        self.today_real_profit_value = self.ui_util.make_entry(
            "\\0", Position(5, 0, 150, 25), today_real_profit_label, title, True
        )

        self.start_trading_btn = self.ui_util.make_button(
            "íŽėėė(Start Trading)",
            Position(150, 0, 250, 25),
            cst_x=self.today_real_profit_value,
            cst_y=title,
            onclick=self.start_trading
        )
        self.stop_trading_btn = self.ui_util.make_button(
            "íŽėė ė§(Stop Trading)",
            Position(20, 0, 250, 25),
            cst_x=self.start_trading_btn,
            cst_y=title,
            status="disabled",
            onclick=self.stop_trading
        )
        self.ui_util.make_button(
            "ėĶė ėëĄęģ ėđĻ(Refresh Now)",
            Position(20, 0, 200, 25),
            cst_x=self.stop_trading_btn,
            cst_y=title,
            onclick=self.refresh
        )

        watching_list_label = self.ui_util.make_label(
            "ę°ėėĒëŠĐ (Watching Stocks)",
            Position(20, 20, 775, 25),
            cst_x=None,
            cst_y=cash_balance_label
        )
        self.watching_list_treeview = self.ui_util.make_treeview(
            ["code", "market", "category", "name", "price", "volume", "unit"],
            ["ėĒëŠĐID", "ėėĨ", "ėėĒ/íë§", "ėĒëŠĐëŠ", "íėŽę°", "ęą°ëë", "íļę°ëĻė"],
            [50, 100, 150, 150, 125, 125, 73],
            Position(20, 5, 775, 300),
            cst_x=None,
            cst_y=watching_list_label
        )
        self.watching_list_treeview.bind("<Double-1>", self.open_stock_detail)

        add_stock_btn = self.ui_util.make_button(
            "ę°ėėĒëŠĐ ėķę°(Add Stock for Watching)",
            Position(20, 0, 225, 25),
            cst_x=None,
            cst_y=self.watching_list_treeview,
            onclick=self.open_add_stock_to_watch_list
        )
        self.ui_util.make_label(
            "ę°ė ėĒëŠĐ ė ëģīė íļė§ęģž ė ęą°ë ëŠĐëĄėė íīëđ ėĒëŠĐė ëëļ íīëĶ­íėŽ ėĪííĐëëĪ.\n"
            + "Double click a stock from the list to remove from it or modify details",
            Position(10, 0, 490, 35),
            cst_x=add_stock_btn,
            cst_y=self.watching_list_treeview
        )

        stock_balance_label = self.ui_util.make_label(
            "íėŽėĢžėėęģ  (Current Stock Balance)",
            Position(20, 45, 775, 25),
            cst_x=None,
            cst_y=self.watching_list_treeview
        )
        self.stock_balance_treeview = self.ui_util.make_treeview(
            ["code", "name", "holdings", "price", "avr_bid_price", "bid_price", "eval_price", "profit_price"],
            ["ėĒëŠĐID", "ėĒëŠĐëŠ", "ëģīė ėë", "íėŽę°", "íę· ë§Īėę°", "ë§ĪėęļėĄ", "íę°ęļėĄ", "íę°ėėĩęļėĄ"],
            [50, 150, 75, 100, 100, 100, 100, 98],
            Position(20, 5, 775, 300),
            cst_x=None,
            cst_y=stock_balance_label
        )

        order_logs_label = self.ui_util.make_label(
            "ėëėĢžëŽļëīė­ (Automated Order Logs)",
            Position(20, 20, 775, 25),
            cst_x=self.watching_list_treeview,
            cst_y=cash_balance_label
        )
        self.order_logs_treeview = self.ui_util.make_treeview(
            ["code", "name", "type", "price", "quantity", "timestamp", "tx_no"],
            ["ėĒëŠĐID", "ėĒëŠĐëŠ", "ë§Īė/ë§Īë", "ėĢžëŽļę°", "ėĢžëŽļėë", "ėĢžëŽļėę°", "ėĢžëŽļëēíļ"],
            [50, 150, 75, 75, 75, 100, 248],
            Position(20, 5, 775, 675),
            cst_x=self.watching_list_treeview,
            cst_y=order_logs_label
        )

    def reload_current_cash_balance(self):
        try:
            self.cash_balance_value.configure(state="normal")
            self.cash_balance_value.delete(0, "end")
            self.cash_balance_value.insert(
                0, "\\" + format(self.stock_watch_serv.get_balance_serv().fetch_cash_balance(), ',')
            )
            self.cash_balance_value.configure(state="readonly")
        except Exception:
            self.cash_balance_value.configure(state="normal")
            self.cash_balance_value.delete(0, "end")
            self.cash_balance_value.insert(0, "ERROR")
            self.cash_balance_value.configure(state="readonly")

    def reload_today_profit_realize(self):
        realied_profit_total = 0
        for row in self.stock_balance_treeview.get_children():
            if (
                    self.stock_balance_treeview.item(row) is not None
                    and self.stock_balance_treeview.item(row)["values"] is not None
                    and self.stock_balance_treeview.item(row)["values"][7] is not None
                    and type(self.stock_balance_treeview.item(row)["values"][7]) is int
            ):
                realied_profit_total += self.stock_balance_treeview.item(row)["values"][7]
        self.today_real_profit_value.configure(state="normal")
        self.cash_balance_value.delete(0, "end")
        self.cash_balance_value.insert(0, "\\" + format(realied_profit_total, ','))
        self.today_real_profit_value.configure(state="readonly")

    def reload_watching_stock_treeview(self):
        for child in self.watching_list_treeview.get_children():
            self.watching_list_treeview.delete(child)
        for stock in self.stock_watch_serv.get_watching_list():
            self.watching_list_treeview.insert("", "end", values=(
                stock.get_code(), stock.get_market(), stock.get_category(), stock.get_name(),
                stock.get_price(), stock.get_volume(), stock.get_bid_unit()
            ))

    def reload_stock_balance_treeview(self):
        stock_balance_service = self.stock_watch_serv.get_balance_serv()
        for child in self.stock_balance_treeview.get_children():
            self.stock_balance_treeview.delete(child)
        for balance_row in stock_balance_service.fetch_stock_balance():
            self.stock_balance_treeview.insert("", "end", values=balance_row)

    def reload_order_logs_treeview(self):
        auto_trader = self.stock_watch_serv.get_auto_trader()
        for child in self.order_logs_treeview.get_children():
            self.order_logs_treeview.delete(child)
        for order in auto_trader.get_order_list()[::-1]:
            self.order_logs_treeview.insert("", "end", values=order.get_order_detail_row())

    def open_add_stock_to_watch_list(self):
        if self.stock_watch_serv.get_task() is not None and not self.stock_watch_serv.get_task().done():
            tkinter.messagebox.showerror(
                "Error", "íŽė ėĒëŠĐė ëģęē―íęļ° ė ė ëĻžė  ėë íŽėëĨž ė ė§ íė­ėėĪ\n"
                + "Stop auto trading before to change watching stocks"
            )
        else:
            StockRegisterUI(self, self.stock_watch_serv).setup()

    def open_stock_detail(self, _):
        StockDetailUI(
            self, self.stock_watch_serv,
            self.watching_list_treeview.index(self.watching_list_treeview.selection()[0])
        ).setup()

    def start_trading(self):
        self.start_trading_btn.config(state="disabled")
        self.stop_trading_btn.config(state="normal")
        self.stock_watch_serv.start_watching()

    def stop_trading(self):
        self.stop_trading_btn.config(state="disabled")
        self.start_trading_btn.config(state="normal")
        self.stock_watch_serv.stop_watching()

    def refresh(self, auto_refresh=True):
        self.reload_current_cash_balance()
        self.reload_watching_stock_treeview()
        self.reload_stock_balance_treeview()
        self.reload_order_logs_treeview()
        self.reload_today_profit_realize()
        if auto_refresh:
            self.task = self.after(5000, self.refresh)

    def close(self):
        # ëĢĻíę° ėĪí ėĪėļ ęē―ė° ę°ė  ėĪė§
        self.after_cancel(self.task)
        if self.stock_watch_serv.get_task() is not None and not self.stock_watch_serv.get_task().done():
            self.stock_watch_serv.stop_watching()
        self.destroy()
        self.parent.deiconify()
