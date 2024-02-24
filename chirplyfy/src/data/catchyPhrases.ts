export interface ICatchyUploadPhrase {
  main: string
  secondary: string
}

const catchyPhrases: ICatchyUploadPhrase[] = [
  {
    main: "Sing us a tune, we'll sing you two!",
    secondary: "Upload your bird song and discover its crew."
  },
  {
    main: "Chirp us a melody, we'll find its harmony!",
    secondary: "Upload your song and join the symphony."
  },
  {
    main: "Got a feathered friend's refrain?",
    secondary: "Upload and find its feathered strain!"
  },
  {
    main: "Confused by that birdie's beat?",
    secondary: "Upload its song, we'll help you meet!"
  },
  {
    main: "Unlock the mystery:",
    secondary: "Upload your bird song, find its feathered family!"
  },
  {
    main: "Curiosity chirping?",
    secondary: "Let Chirplyfy identify your bird by its song! Upload now!"
  },
  {
    main: "Lost in the avian chorus?",
    secondary: "Upload your bird song, let Chirplyfy guide you soaring!"
  },
  {
    main: "Discover the wonders of bird songs:",
    secondary: "Upload yours and explore the feathered world!"
  },
  {
    main: "Upload & Identify:",
    secondary: "Let your bird's song be your guide."
  },
  {
    main: "Sing it like a bird:",
    secondary: "Upload and find its kindred spirit."
  },
  {
    main: "Unlock the melody:",
    secondary: "Upload your bird song, explore its symphony."
  },
  {
    main: "Chirp, sing, upload:",
    secondary: "Discover the birds you couldn't name."
  },
]

export const getCatchyUploadPhrase = () => {
  return catchyPhrases.at(Math.floor(Math.random() * catchyPhrases.length)) || catchyPhrases[0]
}