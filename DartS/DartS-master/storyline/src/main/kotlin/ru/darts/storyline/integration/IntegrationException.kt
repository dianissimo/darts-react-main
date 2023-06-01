package ru.darts.storyline.integration

class IntegrationException(message: String?, cause: Throwable?) : Throwable(message, cause) {
    constructor(message: String?) : this(message, null)
}
