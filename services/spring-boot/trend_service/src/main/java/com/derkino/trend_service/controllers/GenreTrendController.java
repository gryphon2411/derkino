package com.derkino.trend_service.controllers;

import com.derkino.trend_service.common.Utils;
import org.apache.kafka.streams.KeyValue;
import org.apache.kafka.streams.StoreQueryParameters;
import org.apache.kafka.streams.kstream.Windowed;
import org.apache.kafka.streams.state.KeyValueIterator;
import org.apache.kafka.streams.state.QueryableStoreTypes;
import org.apache.kafka.streams.state.ReadOnlyWindowStore;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.config.StreamsBuilderFactoryBean;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.Duration;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

@RestController
public class GenreTrendController {
    private static final Logger logger = LoggerFactory.getLogger(GenreTrendController.class);

    @Autowired
    StreamsBuilderFactoryBean bean;

    @GetMapping("/trends/genres")
    public Map<String, Long> getGenreTrends(@RequestParam(value = "minutes", defaultValue = Utils.MIN_WINDOW_TIME_MINUTES) long minutes) {
        StoreQueryParameters<ReadOnlyWindowStore<String, Long>> parameters = StoreQueryParameters.fromNameAndType(
                "genre-counts",QueryableStoreTypes.windowStore()
        );

        ReadOnlyWindowStore<String, Long> windowStore = bean.getKafkaStreams().store(parameters);

        Instant currentTime = Instant.ofEpochMilli(System.currentTimeMillis());
        Instant timeFrom = currentTime.minus(Duration.ofMinutes(minutes));

        Map<String, Long> trends = new HashMap<>();
        KeyValueIterator<Windowed<String>, Long> iterator = windowStore.fetchAll(timeFrom, currentTime);
        while (iterator.hasNext()) {
            KeyValue<Windowed<String>, Long> next = iterator.next();
            trends.put(next.key.key(), next.value);
            logger.info(
                    "\n\n getGenreTrends" +
                            "\n next: " + next +
                            "\n next.key: " + next.key +
                            "\n next.key.key(): " + next.key.key() +
                            "\n next.key.window(): " + next.key.window() +
                            "\n next.value: " + next.value
            );
        }

        return trends;
    }
}
