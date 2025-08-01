// frontend/src/components/NewsFeed.js
import React from 'react';
import { formatDistanceToNow } from 'date-fns';

function NewsFeed({ news, symbol }) {
  if (!symbol) return null; // Don't render if no symbol is selected

  return (
    <div className="bg-light-content dark:bg-dark-content rounded-lg shadow-md mt-6 p-4">
      <h2 className="text-xl font-semibold text-light-text-strong dark:text-dark-text-strong mb-4">
        Latest News for {symbol}
      </h2>
      {!news ? (
        <p>Loading news...</p>
      ) : news.length === 0 ? (
        <p>No news found for {symbol}.</p>
      ) : (
        <ul className="space-y-4">
          {news.map((article) => (
            <li key={article.uuid} className="border-b border-light-base dark:border-dark-base pb-4 last:border-b-0">
              <a href={article.link} target="_blank" rel="noopener noreferrer" className="hover:underline">
                <h3 className="font-bold text-light-accent dark:text-dark-accent">{article.title}</h3>
              </a>
              <div className="text-xs text-gray-500 dark:text-gray-400 mt-1 flex justify-between">
                <span>{article.publisher}</span>
                <span>{formatDistanceToNow(new Date(article.provider_publish_time * 1000), { addSuffix: true })}</span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default NewsFeed;