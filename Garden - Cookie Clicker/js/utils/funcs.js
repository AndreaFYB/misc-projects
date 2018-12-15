import moment from moment;

const extensions = [
    "million", "billion", "trillion", "quadrillion",
    "quintillion", "sextillion", "septillion",
    "octillion", "nonillion", "decillion",
    "undecillion", "duodecillion", "tredecillion",
    "quattordecillion", "quindecillion", "sexdecillion"
]

export function numToWord(num){
    sNum = num / (10 ** 6)

    if (sNum < 1) return num;

    let i;

    for(i = 0; sNum / 1000 >= 1 && i <= 15; i++){
        sNum /= 1000;
    }

    return `${sNum.toFixed(3)} ${extensions[i]}`
}

export function wordToNum(num, extension){
    let exps = []

    for(let i = 6; i <= 52; i+=3){
        exps.push(10 ** i);
    }

    let obj = {}

    for(let i in extensions){
        obj[extensions[i]] = exps[i];
    }

    return num * obj[extension];
}

export function calculateTotalChance(wc, p1, p2, empty, mutRate, mutName){
    // to be implemented
}

export function getTime(prompt, offset=0){
    return `${prompt}${moment().add(offset, 'seconds').format("MMMM Do YYYY, hh:mm:ss")}`
}