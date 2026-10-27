// fetch("API", {
//   method : "POST",
//   header:{
//     "authorization": `Bearer ${token}`
//     }
// })

const auth = (req, res, next) => {
    const temp = req.header.authorization // "Bearer token"

    const token = temp.split(" ")[1]  // ["Bearer", "token"]

    const flag = jwt.verify(token, process.env.SECRET_KEY)
}