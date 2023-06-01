package ru.darts.storyline.integration

import org.junit.jupiter.api.Test


import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest


@SpringBootTest
internal class DbAdapterIntegrationTest {
    @Autowired
    lateinit var dbAdapter: DbAdapter

    @Test
    fun getLongreadEventsOkTest() {
        print(dbAdapter.getLongreadEvents(1))
    }

    @Test
    fun getLongreadEventTest() {
        print(dbAdapter.getEvent(1))
    }

    @Test
    fun updateEventOfBlockContentTest() {
        print(dbAdapter.updateEventOfBlockContent(1, 4, 9, 123, "Something hapoend 1"))
    }

    @Test
    fun deleteEventOfBlockContentTest() {
        print(dbAdapter.deleteEventOfBlockContent(1))
    }

    @Test
    fun getMapImgUrlTest() {
        print(dbAdapter.getMapImgUrl(1))
    }


    @Test
    fun getTimelineImgUrlTest() {
        print(dbAdapter.getTimelineImgUrl(1))
    }


}