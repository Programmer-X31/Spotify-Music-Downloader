from spotify_downloader import Spotify_Downloader
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import tkinter as tk


class Styles:
    TITLE_FONT = ('Noto Sans', 20, 'bold')
    FONT = ('Noto Sans', 10)
    PADDING_X = 8
    PADDING_Y = 5
    MARGIN_X = 2
    MARGIN_Y = 2


class Frontend_GUI(tk.Tk):
    def draw_gui(self):
        # Title
        tk.Label(text="Spotify Music Downloader", font=Styles.TITLE_FONT).grid(
            row=0, column=0, columnspan=5, rowspan=2)

        # Spotify Secret
        self.LABEL(text="Spotify Secret:", row=2, col=0)
        tk.Entry(width=50, textvariable=self.sp_secret).grid(row=2, column=2, columnspan=3,
                                                             ipadx=Styles.PADDING_X, ipady=Styles.PADDING_Y, padx=Styles.MARGIN_X, pady=Styles.MARGIN_Y)

        self.LABEL(text="Spotify Client ID:", row=3, col=0)
        tk.Entry(width=50, textvariable=self.sp_api_key).grid(row=3, column=2, columnspan=3,
                                                              ipadx=Styles.PADDING_X, ipady=Styles.PADDING_Y, padx=Styles.MARGIN_X, pady=Styles.MARGIN_Y)

        # Playlist Name
        self.LABEL(text="Playlist Link:", row=4, col=0)
        tk.Entry(width=50, textvariable=self.playlist).grid(row=4, column=2, columnspan=3,
                                                            ipadx=Styles.PADDING_X, ipady=Styles.PADDING_Y, padx=Styles.MARGIN_X, pady=Styles.MARGIN_Y)

        # Spotify API Key
        # Location
        self.LABEL(text="Location:", row=5, col=0)
        tk.Entry(width=50, textvariable=self.location).grid(row=5, column=2, columnspan=3,
                                                            ipadx=Styles.PADDING_X, ipady=Styles.PADDING_Y, padx=Styles.MARGIN_X, pady=Styles.MARGIN_Y)
        # Submit Button TODO Finish the Submit Button
        tk.Button(text="Start Download", command=self.handle_submit, bg="#00aabb").grid(
            row=7, column=0, columnspan=5)

        # Output
        labelframe = tk.LabelFrame(font=Styles.FONT)
        labelframe.grid(
            row=8, column=0, columnspan=5, rowspan=5, sticky='WE', padx=10, pady=10, ipadx=110, ipady=10)

        tk.Label(labelframe, text="Successfully Downloaded:", font=Styles.FONT, fg="#00af00").grid(
            ipadx=Styles.PADDING_X, ipady=Styles.PADDING_Y, row=7, column=0, columnspan=2)

        tk.Label(labelframe, text="Failed to Download:", font=Styles.FONT, fg="#ff0000").grid(
            ipadx=Styles.PADDING_X, ipady=Styles.PADDING_Y, row=8, column=0, columnspan=2)

        tk.Label(labelframe, text="Remaining for Download:", font=Styles.FONT).grid(
            ipadx=Styles.PADDING_X, ipady=Styles.PADDING_Y, row=9, column=0, columnspan=2)

        self.successful_download_label = tk.Label(
            labelframe, text="Not Available", font=Styles.FONT, fg="#00af00")
        self.failed_download_label = tk.Label(
            labelframe, text="Not Available", font=Styles.FONT, fg="#ff0000")
        self.remaining_tracks = tk.Label(
            labelframe, text="Not Available", font=Styles.FONT)

        self.successful_download_label.grid(
            ipadx=Styles.PADDING_X, ipady=Styles.PADDING_Y, row=7, column=2, columnspan=2)
        self.failed_download_label.grid(
            ipadx=Styles.PADDING_X, ipady=Styles.PADDING_Y, row=8, column=2, columnspan=2)
        self.remaining_tracks.grid(
            ipadx=Styles.PADDING_X, ipady=Styles.PADDING_Y, row=9, column=2, columnspan=2)

        # Drawing the components on screen
        self.mainloop()

    def handle_submit(self):
        self.sp_dwn.start_download_process(
            self.sp_api_key.get(), self.sp_secret.get(), self.playlist.get())
        # Selenium
        opt = webdriver.ChromeOptions()
        opt.headless = True  # Does not open new windows during automation
        driver = webdriver.Chrome(options=opt, service=Service(
            ChromeDriverManager().install()))  # Usage of ChromeDriverManager to remove redundancy of downloading driver

        BASE_URL = "https://www.youtube.com/results?search_query="
        for track_name, artist_name, album_name in self.sp_dwn.data_playlist:
            search_term = f"{track_name} - {artist_name}"
            URL = BASE_URL + search_term.replace(" ", "+")
            driver.get(URL)
            driver.implicitly_wait(5)
            title_elem = driver.find_element(
                by=By.XPATH, value='/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a')
            youtube_url = title_elem.get_attribute("href")
            self.sp_dwn.audio_download_pytube(
                youtube_url, artist_name, album_name, track_name, self.location.get())

            self.successful_download_label.configure(
                text=str(self.sp_dwn.audio_download_success_count))
            self.successful_download_label.update()
            self.failed_download_label.configure(
                text=str(self.sp_dwn.audio_download_failure_count))
            self.failed_download_label.update()
            self.remaining_tracks.configure(
                text=str(self.sp_dwn.audio_remaining_count))
            self.remaining_tracks.update()

        tk.Label(text="Finished Process!", font=('Noto Sans', 15, 'bold')).grid(
            row=14, column=1, columnspan=4)
        print("[*] Completed Download Process. You may close the window now.")

    def LABEL(self, **kwargs):
        _row = 0  # Row
        _col = 0  # Column
        _text = ""
        if kwargs.__contains__("row"):
            _row = kwargs["row"]
        if kwargs.__contains__("col"):
            _col = kwargs["col"]
        if kwargs.__contains__("text"):
            _text = kwargs["text"]

        return (tk.Label(text=_text, font=Styles.FONT).grid(ipadx=Styles.PADDING_X, ipady=Styles.PADDING_Y, row=_row, column=_col, columnspan=2))

    def __init__(self):
        super().__init__()
        self.title('Spotify Music Downloader')
        self.geometry('540x365')
        self.sp_dwn = Spotify_Downloader()

        self.sp_secret = tk.StringVar()
        self.sp_api_key = tk.StringVar()
        self.playlist = tk.StringVar()
        self.location = tk.StringVar()

        self.draw_gui()


gui = Frontend_GUI()
