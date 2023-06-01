package ru.darts.storyline.conroller

import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController
import ru.darts.storyline.integration.DbAdapter

@RestController
class HelloWorldController {
    @Autowired
    lateinit var dbAdapter: DbAdapter

    private val log = LoggerFactory.getLogger(HelloWorldController::class.java)

    @GetMapping("/hello")
    fun hello() : String {
        log.warn("get yo there!")
        return "hella hi!"
    }
}