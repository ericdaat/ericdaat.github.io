---
layout: post
title: Auto deploy a static website on AWS S3 using CircleCI
date: 2019-04-12
excerpt:
    In this post we are going to look at how to use CircleCI to automatically deploy a static website hosted on AWS S3. AWS S3 is an easy and cheap way to host a static website, and combined with Cloudfront and Route 53 we can have a highly reliable and secure website. CircleCI is a continuous integration tool, which we will use with Github to push the code to AWS S3 at every commit.
cover: writer.jpg
---

In this post we are going to look at how to use CircleCI to automatically deploy a static website hosted on AWS S3. AWS S3 is an easy and cheap way to host a static website, and combined with Cloudfront and Route 53 we can have a highly reliable and secure website. CircleCI is a continuous integration tool, which we will use with Github to push the code to AWS S3 at every commit.

Before getting started, I encourage you to get familiar (if you're not already) with the different tools we are going to use, namely:

- [Amazon Web Services](https://aws.amazon.com/) (AWS): A major Cloud Computing vendor
- [AWS S3](https://aws.amazon.com/s3/): Object storage service from AWS. It can be configured to host static websites.
- [AWS Cloudfront](https://aws.amazon.com/cloudfront): AWS Content Delivery Network (CDN). We will use this to add SSL to our website.
- [AWS Certificate Manager](https://aws.amazon.com/certificate-manager/): AWS service for getting SSL certificates.
- [AWS Route 53](https://aws.amazon.com/route53): Domain Name System (DNS) web service. It is not mandatory to use this, but it makes things easier.
- [Github](https://gitub.com): The most popular hosting service for version control using Git.
- [CircleCI](https://circleci.com/): Continuous Integration (CI) and delivery platform.

## Hosting the website on S3

Note: There are many great tutorials on how to host a static website on AWS S3, so I won't enter into too much details as the main goal of this post is to show how to use CircleCI to synchronize Github and S3.

We assume you already have a static website ready. If not, it can be as simple as `echo "<p>Hello World</p>" > index.html`. You will also need to host your code in Github.

To learn how to host a static website on S3, please follow Step 2 from this page: [Setting up a Static Website Using a Custom Domain](https://docs.aws.amazon.com/AmazonS3/latest/dev/website-hosting-custom-domain-walkthrough.html).

## Create a Cloudfront distribution

Once your bucket is ready and has your website in it, you should use a Cloudfront distribution and a SSL certificate to enable HTTPS. You can discover how to do so here: [How do I use CloudFront to serve a static website hosted on Amazon S3?](https://aws.amazon.com/premiumsupport/knowledge-center/cloudfront-serve-static-website/).

## Using a custom domain name

This step assumes you have bought a domain name (not necessarily from AWS, I bought mine from [Namecheap](https://www.namecheap.com/)).

I prefer using AWS Route 53 for DNS management as it makes things simpler. If you bought your domain name on AWS you don't need any additional configuration. Otherwise, you will need to tell your domain name provider to use AWS name servers.

Let's say you bought `example.com` on Namcheap. You will first need to create a hosted zone on AWS Route 53 named `example.com`. After that, you'll see `NS` records corresponding to the AWS Name Servers, they might look like this:

``` bash
ns-995.awsdns-60.net.
ns-1903.awsdns-45.co.uk.
ns-155.awsdns-19.com.
ns-1306.awsdns-35.org.
```

You'll want to add these to Namecheap, as explained here: [How to Change DNS For a Domain](https://www.namecheap.com/support/knowledgebase/article.aspx/767/10/how-to-change-dns-for-a-domain).

Now Namecheap will redirect to Route53, but you'll need to tell Route53 what to redirect the trafic to. Create record sets like `www.example.com` and `example.com` and make them point to your Cloudfront distribution.

We are done for the first part, your website hosted in S3 should show at `example.com`. Again, we skipped some details for this part as it is not the main goal of this post. Some tutorials explain this part much better than I did. I recommend these ones:

- [How to Host a Website on S3 Without Getting Lost in the Sea](https://medium.freecodecamp.org/how-to-host-a-website-on-s3-without-getting-lost-in-the-sea-e2b82aa6cd38)
- [How to host your static website with S3 & CloudFront and set-up an SSL certificate?](https://medium.com/devopslinks/how-to-host-your-static-website-with-s3-cloudfront-and-set-up-an-ssl-certificate-9ee48cd701f9)

## Setting up CircleCI and Github

Here's the exciting part: whenever you push changes to Github, CircleCI will sync the code files with the AWS S3 bucket you created.

We assume you alrady have your static website hosted on Github. If you haven't already, sign up to CircleCI (it's free), and add your Github repo to a CircleCI project.

CircleCI uses `awscli` to sync files with S3, so it requires credentials to login to your AWS account. Go to AWS IAM, and [create a `circleci` user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_cliwpsapi), with restricted permissions on your S3 bucket.

When you finish creating the user, you will be given credentials (an ID key and a secret key) that you should store somewhere safe. You will also need to store these as environment variables in CircleCI. Go to your project settings, and under environment variables, add these variables, corresponding to the ones you just downloaded:

- AWS_ACCESS_KEY
- AWS_SECRET_ACCESS_KEY
- AWS_REGION

Now CircleCI will login to you AWS account with the user you created, and it will have the right permissions to push files to your S3 bucket.

Finally, you'll need to add this configuration file to your Github repository, under `.circleci/config.yml`:

``` bash
version: 2.1
orbs:
  aws-s3: circleci/aws-s3@1.0.6

jobs:
  build:
    docker:
      - image: 'circleci/python:latest'

    steps:
      - checkout
      - aws-s3/sync:
          from: .
          to: 's3://your-bucket'
          arguments: |
            --acl public-read \
            --cache-control "max-age=86400" \
            --exclude ".git/*" \
            --exclude ".gitignore" \
            --exclude ".circleci/*" \
          overwrite: true
```

Adapt this configuration file to your needs, by changing the S3 bucket url, and modify the files to exclude by the sync command.

When that's done, push to Github, and see that the pipeline runs correctly on CircleCI. When it succeeds, you should see your files updated on AWS S3.

Have a look at my [personnal website repository](https://github.com/ericdaat/edaoud.com) for more details.

I hope this post was helpful, let me know if you need any help, or if something does not seem right.
