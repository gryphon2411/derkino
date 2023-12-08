package com.derkino.trend_service.controllers;

import com.derkino.trend_service.TrendServiceApplication;
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
import org.springframework.web.bind.annotation.RestController;

import java.time.Duration;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

@RestController
public class TrendController {
    private static final Logger logger = LoggerFactory.getLogger(TrendServiceApplication.class);
    @Autowired
    StreamsBuilderFactoryBean bean;

    @GetMapping("/trends")
    public Map<String, Long> getTrends() {
        Map<String, Long> trends = new HashMap<>();
        StoreQueryParameters<ReadOnlyWindowStore<String, Long>> parameters = StoreQueryParameters.fromNameAndType(
                "kafka-streams-state-store",QueryableStoreTypes.windowStore()
        );

        ReadOnlyWindowStore<String, Long> windowStore = bean.getKafkaStreams().store(parameters);

        // Get the window end timestamp
        Instant timeTo = Instant.ofEpochMilli(System.currentTimeMillis()); // current time
        Instant timeFrom = timeTo.minus(Duration.ofMinutes(3)); // beginning of window

        // Query the window store for the latest counts
        KeyValueIterator<Windowed<String>, Long> iterator = windowStore.fetchAll(timeFrom, timeTo);
        while (iterator.hasNext()) {
            KeyValue<Windowed<String>, Long> next = iterator.next();
            trends.put(next.key.toString(), next.value);
        }

        return trends;
    }
}
