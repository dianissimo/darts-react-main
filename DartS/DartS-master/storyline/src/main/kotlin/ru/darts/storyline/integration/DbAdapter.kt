package ru.darts.storyline.integration

import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.boot.web.client.RestTemplateBuilder
import org.springframework.stereotype.Service
import ru.darts.storyline.UniversalTimelineRq


@Service
class DbAdapter(restTemplateBuilder: RestTemplateBuilder) {
    @Value("\${dbClient.base.url:http://127.0.0.1:4000}")
    private lateinit var baseUrl: String
    private val dbClient = restTemplateBuilder.build()
    private val LOG: Logger = LoggerFactory.getLogger(DbAdapter::class.java)
    private val INTEGRATION_ERROR_TEXT: String = "DbAdapter Integration ERROR"


// event
    fun getLongreadEvents(longreadId: Long): String {
        val relativeUrl = "/longread/blockcontent/all"
        LOG.info("getLongreadEvents: $longreadId ; dbClientUrl = $baseUrl, relativeUrl = $relativeUrl")
        val rq = UniversalTimelineRq(null, null, null, null, null, longreadId)

        return sendRequest(baseUrl + relativeUrl, rq, String::class.java)
    }
    fun getEvent(blockContentId: Long): String {
        val relativeUrl = "/longread/blockcontent/event"
        LOG.info("getEvent: $blockContentId ; dbClientUrl = $baseUrl, relativeUrl = $relativeUrl")
        val rq = UniversalTimelineRq(blockContentId, null, null, null, null, null)

        return sendRequest(baseUrl + relativeUrl, rq, String::class.java)
    }

    fun updateEventOfBlockContent(blockContentId: Long, xCoordinate: Long,  yCoordinate: Long, time: Long, floatingText: String) {
        val relativeUrl = "/longread/blockcontent/event/edit"
        LOG.info("updateEventOfBlockContent: $blockContentId ; dbClientUrl = $baseUrl, relativeUrl = $relativeUrl")
        val rq = UniversalTimelineRq(blockContentId, xCoordinate, yCoordinate, time, floatingText, null)
        sendRequest(baseUrl + relativeUrl, rq, String::class.java)
    }

    fun deleteEventOfBlockContent(blockContentId: Long) {
        val relativeUrl = "/longread/blockcontent/event/delete"
        LOG.info("deleteEventOfBlockContent: $blockContentId ; dbClientUrl = $baseUrl, relativeUrl = $relativeUrl")
        val rq = UniversalTimelineRq(blockContentId, null, null, null, null, null)
        sendRequest(baseUrl + relativeUrl, rq, String::class.java)
    }

// map
    fun getMapImgUrl(longreadId: Long): String {
        val relativeUrl = "/longread/map"
        LOG.info("getMapImgUrl: $longreadId ; dbClientUrl = $baseUrl, relativeUrl = $relativeUrl")
        val rq = UniversalTimelineRq(null, null, null, null, null, longreadId)

        return sendRequest(baseUrl + relativeUrl, rq, String::class.java)
    }

// timeline
    fun getTimelineImgUrl(longreadId: Long): String {
        val relativeUrl = "/longread/timeline"
        LOG.info("getTimelineImgUrl: $longreadId ; dbClientUrl = $baseUrl, relativeUrl = $relativeUrl")
        val rq = UniversalTimelineRq(null, null, null, null, null, longreadId)

        return sendRequest(baseUrl + relativeUrl, rq, String::class.java)
    }

//    fun getLongreadEvents(chapterId: String): String  {
//        LOG.info("getLongreadEvents: $chapterId ; dbClientUrl = $baseUrl")
//
//
//        return sendRequest()
//    }




    private inline fun <reified T> sendRequest(url: String, request: Any?, responseType: Class<T>) : T {
        LOG.info("Sending request $request on $url")
        val response = dbClient.postForEntity(url, request, responseType)
        if (response.statusCode.is2xxSuccessful) {
            requireNotNull(response.body)
            LOG.info("Got response: ${response.body}")
            return response.body!!
        }

        LOG.error(INTEGRATION_ERROR_TEXT, "response: $response")
        throw IntegrationException(INTEGRATION_ERROR_TEXT)
    }
}