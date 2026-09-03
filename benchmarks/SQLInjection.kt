// BENCHMARK: SQL Injection
fun vulnerableQuery(db: SQLiteDatabase, userInput: String) {
    db.execSQL("SELECT * FROM users WHERE name = '" + userInput + "'")
}
