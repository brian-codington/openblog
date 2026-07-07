// frontend/src/pages/index.tsx
import type { GetStaticProps } from 'next';
import Head from 'next/head';
import Link from 'next/link';
import { format } from 'date-fns';
import { api } from '../api/client';

interface Post {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  published_at: string;
  author: { name: string };
  tags: { name: string; slug: string }[];
}

interface Props {
  posts: Post[];
}

export default function HomePage({ posts }: Props) {
  return (
    <>
      <Head>
        <title>OpenBlog</title>
        <meta name="description" content="A developer blog powered by OpenBlog" />
      </Head>

      <main className="max-w-3xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold mb-2">OpenBlog</h1>
        <p className="text-gray-500 mb-10">Writing on software, engineering, and open source.</p>

        <div className="space-y-10">
          {posts.map(post => (
            <article key={post.id} className="border-b pb-10">
              <Link href={`/posts/${post.slug}`}>
                <h2 className="text-2xl font-semibold hover:text-indigo-600 transition-colors">
                  {post.title}
                </h2>
              </Link>

              <div className="flex items-center gap-3 text-sm text-gray-500 mt-2 mb-3">
                <span>{post.author?.name}</span>
                <span>·</span>
                <time>{format(new Date(post.published_at), 'MMM d, yyyy')}</time>
              </div>

              {post.excerpt && (
                <p className="text-gray-600 leading-relaxed">{post.excerpt}</p>
              )}

              <div className="flex gap-2 mt-4">
                {post.tags?.map(tag => (
                  <Link
                    key={tag.slug}
                    href={`/tags/${tag.slug}`}
                    className="text-xs bg-gray-100 hover:bg-gray-200 px-3 py-1 rounded-full transition-colors"
                  >
                    {tag.name}
                  </Link>
                ))}
              </div>
            </article>
          ))}
        </div>
      </main>
    </>
  );
}

// ISR — regenerate every 60 seconds
export const getStaticProps: GetStaticProps = async () => {
  try {
    const posts = await api.get('/posts?status=published&limit=20');
    return {
      props: { posts: posts.data },
      revalidate: 60
    };
  } catch {
    return { props: { posts: [] }, revalidate: 60 };
  }
};
