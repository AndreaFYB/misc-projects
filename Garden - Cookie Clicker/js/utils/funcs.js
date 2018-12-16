/* eslint-disable func-style */
/* eslint-disable capitalized-comments */
import moment from "moment";

const extensions = [
    "million", "billion", "trillion", "quadrillion",
    "quintillion", "sextillion", "septillion",
    "octillion", "nonillion", "decillion",
    "undecillion", "duodecillion", "tredecillion",
    "quattordecillion", "quindecillion", "sexdecillion"
];

/**
 * This function converts a long number to the english notation.
 * This notation uses words such as million, billion... all the way
 *  up to sexdecillion (10^52)
 * @param {Number} num - the number to convert to a word
 * @returns {String} the number converted to a phrase. 
 */
export function numToWord(num){
    let sNum = num / (10 ** 6);

    if (sNum < 1) return num;

    let i;

    for(i = 0; sNum / 1000 >= 1 && i <= 15; i++){
        sNum /= 1000;
    }

    return `${sNum.toFixed(3)} ${extensions[i]}`;
}

/**
 * This function is the inverse of numToWord.
 * It converts a number in english notation into a decimal
 *  number that can be used in calculations.
 * @param {Number} num - the number being extended
 * @param {String} extension - the word extension that refers to the size 
 * @returns {Number} - the full decimal number representation
 */
export function wordToNum(num, extension){
    let exps = [];

    for(let i = 6; i <= 52; i+=3){
        exps.push(10 ** i);
    }

    let obj = {};

    for(let i in extensions){
        obj[extensions[i]] = exps[i];
    }

    return num * obj[extension];
}

// not finished
// export function calculateTotalChance(wc, p1, p2, empty, mutRate, mutName){
//     // to be implemented
// }

/**
 * Retrieves the current time and stylizes it with a prompt passed as a parameter.
 * The offset is used to show a time in the future/past.
 * @param {String} prompt - The prompt to show before the time.
 * @param {Number} offset - How many seconds to shift by. positive = forwards, negative = backwards.
 * @returns {String} A time representation.
 */
export function getTime(prompt, offset=0){
    return `${prompt}${moment()
        .add(offset, "seconds")
        .format("MMMM Do YYYY, hh:mm:ss")}`;
}