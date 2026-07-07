// frontend/src/pages/posts/[slug].tsx
import type { GetStaticPaths, GetStaticProps } from 'next';
import Head from 'next/head';
import { format } from 'date-fns';
import { MDXRemote, MDXRemoteSerializeResult } from 'next-mdx-remote';
import { serialize } from 'next-mdx-remote/serialize';
import { api } from '../../api/client';

interface Post {
  id: number;
  title: string;
  slug: string;
  content: string;
  excerpt: string;
  published_at: string;
  author: { name: string; bio: string; avatar: string };
  tags: { name: string; slug: string }[];
}

interface Props {
  post: Post;
  mdxSource: MDXRemoteSerializeResult;
}

export default function PostPage({ post, mdxSource }: Props) {
  return (
    <>
      <Head>
        <title>{post.title} — OpenBlog</title>
        <meta name="description" content={post.excerpt} />
        <meta property="og:title" content={post.title} />
        <meta property="og:description" content={post.excerpt} />
      </Head>

      <article className="max-w-2xl mx-auto px-4 py-12">
        <header className="mb-8">
          <h1 className="text-4xl font-bold mb-4 leading-tight">{post.title}</h1>
          <div className="flex items-center gap-3 text-sm text-gray-500">
            <span>{post.author?.name}</span>
            <span>·</span>
            <time>{format(new Date(post.published_at), 'MMM d, yyyy')}</time>
          </div>
        </header>

        <div className="prose prose-lg max-w-none">
          <MDXRemote {...mdxSource} />
        </div>

        {post.author && (
          <footer className="mt-12 pt-8 border-t flex items-start gap-4">
            {post.author.avatar && (
              <img src={post.author.avatar} alt={post.author.name}
                className="w-14 h-14 rounded-full" />
            )}
            <div>
              <div className="font-semibold">{post.author.name}</div>
              <p className="text-gray-500 text-sm mt-1">{post.author.bio}</p>
            </div>
          </footer>
        )}
      </article>
    </>
  );
}

export const getStaticPaths: GetStaticPaths = async () => {
  const res = await api.get('/posts?status=published&limit=100');
  const paths = res.data.map((post: Post) => ({ params: { slug: post.slug } }));
  return { paths, fallback: 'blocking' };
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  try {
    const res = await api.get(`/posts/${params?.slug}`);
    const post = res.data;
    const mdxSource = await serialize(post.content || '');
    return { props: { post, mdxSource }, revalidate: 60 };
  } catch {
    return { notFound: true };
  }
};
