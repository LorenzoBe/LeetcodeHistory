# LeetcodeHistory
This is a project to generate the users contest history of LeetCode platform.
LeetCode doesn't allow users to visualise a meaningful history of the contests which he joined. Without this history it's difficult to keep track of the learning progress and quickly navigate back to the contests.
The target is to acquire the data from LettCode site and present a "nice to see" and "easy to use" graph to fill the gap.

## Solution design
### Data size
The final design need to consider the following numbers:
- Number of LeetCode users: ~110K, growing
- Number of contests:195 weekly + 28 bi-weekly
- Number of users per contests: < 15K
- Data to be stored for each contest partecipation: contest ID (4 bytes), timestamp (4 bytes), rank (4 bytes), score (1 byte), finish time (< 2 hours, 2 bytes expressing it in seconds) -> 15 bytes

We can consider in average that each user joined 50 contests:
key = 255B * 110K ~ 29 MB
values = 15B * 50 * 110K ~ 83 MB
The total is about 120 MB, not so huge.

### Bandwidth
The backend service will be a read heavy service. The data can be updated unce a week by an administration script, while the data will be retrieved by users to visualise the graph. We can estimate a spike of 15K users in the hour just after a contest. To find the QPS:
READ QPS = 15K / 60 minutes / 60 seconds = 4.2 QPS

The data retrieved by each user is the complete contest history, so:
READ BW = 4.2 QPS * 15B * 50 = 3150 B/s = 26 Kbit/sec

### Storage
We could use an RDBMS database, maybe in master-slave configuration to improve read capabilities and availability. We don't need strict consistency between the two nodes. We could have just two tables: User and Contest. Contest could contain about 5 millions of records.
On the other hand, we don't need to do complex queries on data, we just need the contests results of a single user to visulise them into a graph. A key-value storage with possibility of setting complex values structure (multicolumn, nested types) is probably enought.
Since there are no additional constrains, the availability of the storage types on Cloud providers, the costs, the integration effort and the "it's cool :D" factors will be taken into consideration.


