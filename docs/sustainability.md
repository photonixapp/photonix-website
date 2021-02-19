# Sustainability and the Environment

Building technology that improves the planet for all is a strong ambition held by the founder of this project. We are all nature and everything we do affects one another.

We are a small player in this industry and it can be hard to trace the environmental impact of all services we use but we think it’s important to consider this in all decisions we make. If we are to grow as a sustainable project then it is important to bake these ethics in from the start while we are small. As we use more and more cloud technology we will endeavour to discover and report our findings.

## Hardware (Our Servers)

Generally we try to only provision servers for resources that we expect we will need in the short term. This means running on **virtual servers** where multiple tenants share compute and memory resources rather than owning dedicated machines. For storage this means using scalable resources like object storage APIs so we are not buying our own disks and letting then sit mostly empty.

Our servers that host this website and the demo application are located in Equinix’s LD5 datacenter near London, UK. Their Sustainability Reference Guides for November 2020 and previous years show that they had **100% renewable energy** coverage at least for the years 2017, 2018 and 2019. Their supplier is REGO-backed certified renewable energy which is part of the Ofgem UK government body’s environmental programme.

By using a cloud provider that is reliable, a decent size, and manages their resources well helps to minimise our impact also. This is hard to measure and has to be judged over time. By using quality components, cooling efficiency and looking after many customers, a provider helps to reduce environmental impact through scale.

### Sources

- [DigitalOcean forum discussion](https://www.digitalocean.com/community/questions/what-kind-of-electricity-do-you-run-on?answer=58615)
- [Equinix’s Commitment to Sustainability](https://www.equinix.com/data-centers/design/green-data-centers/)
- [Equinix’s Sustainability Reference Guide (Nov 2020)](https://sustainability.equinix.com/wp-content/uploads/2020/11/GU_IBX-Sustainability-Quick-Reference_US-EN-4.pdf)
- [Equinix’s Sustainability Map](https://sustainability.equinix.com/map-of-initiatives/)
- [Ofgem’s Renewable Energy Guarantees Origin (REGO) Programme](https://www.ofgem.gov.uk/environmental-programmes/rego)


## Software (Our Product)

The software that makes up Photonix uses resources while running. We understand that if we become a popular product running all over the world then this has an environmental impact that we are partially responsible for. We can’t control how people will use our software but we can do things to promote a healthy environment.

1. Make our **software as efficient as possible** and keep up-to-date with latest algorithmic breakthroughs. These tweaks are often in line with improving the user experience such as reducing data sent over mobile networks and making the application more responsive.
2. Give people **control over which types of analysis** are used as AI can be computationally intensive. If someone doesn’t have a need for object recognition, let them turn it off.
3. Give users access to **efficient cloud storage** with encryption rather than run their own hard drives. People should see the benefit of cloud storage without sacrificing photo privacy.
4. Encourage users to consider **when they are using energy**. Users can reduce the number of hours their system is on for. If agile electricity tariffs are available in the user’s area they can save resources by doing heavy processing outside peak hours or when there is surplus energy in the grid (e.g. when it’s windy).
5. Help users **manage and find their photos efficiently** so they aren’t keeping hold of gigabytes of old data they no longer want.
6. Make sure Photonix **runs on low-power** computer architectures like the ARM-based Raspberry Pi. From my own testing, Photonix runnning at idle on the latest Raspberry Pi 4 Model B consumes 3.8W without external devices.

We use some additional third party tools to run the project. Examples of this are [GitHub](https://github.com/) for code hosting and project management, [Travis](https://travis-ci.org/) for continuous integration testing and [Docker Hub](https://hub.docker.com/) for software deployment. We believe that because these are large services with multiple tenants and we use them for short periods at a time, this is more efficient than hosting our own alternatives.

We'd be happy to hear if you have any more suggestions.
