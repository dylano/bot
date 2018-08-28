const reddit = require('snoowrap');

const getHeadlines = () => {
  return `<b>Headlines</b> from <a href="https://www.reddit.com/r/oaklandraiders/">r/oaklandraiders</a>:
    * Georgio Tavecchio signs with Atlanta. (<a href="https://www.reddit.com/r/oaklandraiders/comments/9apyuv/georgio_tavecchio_signs_with_atlanta/">Read</a>)
    * Donald Penn also said that when Jon Gruden dials down practice intensity, Penn tells the DE he's facing to go harder since he wants to make up for the right tackle reps he missed at start of camp.(<a href="https://www.reddit.com/r/oaklandraiders/comments/9at36m/donald_penn_also_said_that_when_jon_gruden_dials/">Read</a>)
    `;
};

module.exports = getHeadlines;
