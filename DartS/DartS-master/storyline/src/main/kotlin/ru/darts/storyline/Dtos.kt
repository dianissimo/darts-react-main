package ru.darts.storyline

import com.fasterxml.jackson.annotation.JsonAutoDetect
import com.fasterxml.jackson.annotation.JsonInclude
import com.fasterxml.jackson.annotation.JsonProperty

@JsonInclude(JsonInclude.Include.NON_EMPTY)
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
data class UniversalTimelineRq(
    @JsonProperty("blockcontent_id") var blockContentId: Long?,
    @JsonProperty("coordx") var xCoordinate: Long?,
    @JsonProperty("coordy") var yCoordinate: Long?,
    var time: Long?,
    @JsonProperty("floating_text") var floatingText: String?,
    @JsonProperty("longread_id") var longreadId: Long?
)