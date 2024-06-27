import concurrent.futures
from flask import render_template, request
from .scrapers.carrefour_scraper import scrape_carrefour
from .scrapers.hyperone_scraper import scrape_hyperone
from .scrapers.oscar_scraper import scrape_oscar

def init_app(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/search', methods=['POST'])
    def search():
        search_term = request.form['search_term']
        scrapers = [scrape_carrefour, scrape_hyperone, scrape_oscar]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_scraper = {executor.submit(scraper, search_term): scraper for scraper in scrapers}
            results = []
            for future in concurrent.futures.as_completed(future_to_scraper):
                scraper_results = future.result()
                if scraper_results:
                    results.extend(scraper_results)

        return render_template('results.html', results=results)
