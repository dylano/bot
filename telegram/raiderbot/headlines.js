const axios = require('axios');
const HEADLINE_URL = 'https://www.reddit.com/r/oaklandraiders.json';
const NUM_HEADLINES = 5;

const getHeadlines = async () => {
  const allHeadlines = (await axios.get(HEADLINE_URL)).data.data.children;

  const topTitles = allHeadlines
    .filter((x, i) => i <= NUM_HEADLINES - 1)
    .map(
      headline =>
        `* ${headline.data.title} (<a href="https://www.reddit.com/${
          headline.data.permalink
        }">Read</a>)\n`
    );

  let result = `<b>Headlines</b> from <a href="https://www.reddit.com/r/oaklandraiders/">r/oaklandraiders</a>:\n`;
  topTitles.forEach(element => {
    result = result.concat(element);
  });

  return result;
};

module.exports = getHeadlines;
