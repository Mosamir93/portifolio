"""
This file contains route definitions for the Flask application.
"""
from flask import render_template, request
from .scrapers.carrefour_scraper import scrape_carrefour
from .scrapers.hyperone_scraper import scrape_hyperone
from .scrapers.oscar_scraper import scrape_oscar
import concurrent.futures
import re

def init_app(app):
    """
    Initialize the routes for the Flask app.
    """
    @app.route('/')
    def index():
        """Render the homepage"""
        return render_template('index.html')

    @app.route('/search', methods=['POST'])
    def search():
        """
        Handle search requests, perform web scraping, and
        render the results page.
        """
        search_term = request.form['search_term']
        scrapers = [scrape_carrefour, scrape_hyperone, scrape_oscar]
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_scraper = {
                executor.submit(scraper, search_term): scraper
                for scraper in scrapers
            }
            results = []
            for future in concurrent.futures.as_completed(future_to_scraper):
                scraper_results = future.result()
                if scraper_results:
                    results.extend(scraper_results)
            results = sorted(
                results, key=lambda x: float(re.sub(r'[^\d.]', '', x['price']).replace(',', '')))
            no_results = len(results) == 0
        return render_template(
            'results.html', results=results, search_term=search_term, no_results=no_results)
